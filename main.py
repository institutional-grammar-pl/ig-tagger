import click
from igannotator.output.tsv import write_tsv_representation
from igannotator.annotator.ig_annotator import IgAnnotator


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
@click.argument("layer", required=False, default="both")
@click.argument("language", default="en", required=False)
@click.argument("output_format", default="tsv", required=False)
@click.argument("save_connlu", default=False, required=False)
def annotate_file(input, output, language, output_format, layer, save_connlu):

    if language != "en":
        exit('Unsopperted language. At the moment only annotations of english text are supported.')
    if output_format != "tsv":
        exit('Unsopperted output format. At the moment output to tsv file is supported.')
    if layer not in ['reg', 'cons', 'both']:
        exit('Unsopperted layer type. At the moment only "reg", "cons", "both" values are supported')

    with open(input, "r") as f:
        input_text = f.read()

    if layer in ['reg', 'cons']:
        layers = [layer]
    else:
        layers = ['reg', 'cons']

    annotator = IgAnnotator(language, layers)
    sentences = [x for x in input_text.split("\n\n") if len(x) > 0]
    data = list()
    current_component_id = 1
    level_id = 1

    if save_connlu:
        connlu_output = 'data/connlu/' + input.split('/')[-1][:-4]+"_connlu.txt"
        connlu_out = open(connlu_output, "w")

    final_layers = set()
    for sentence in sentences:
        if save_connlu:
            connlu_out.write(annotator.get_connlu_sentence(sentence))
            connlu_out.write('\n')
        tree, tags, current_component_id, used_layers = annotator.annotate_sentence(sentence, current_component_id, level_id, layers)
        data.append((sentence, tree, tags))
        final_layers.update(used_layers)

    if save_connlu:
        connlu_out.close()

    if output_format == 'tsv':
        write_tsv_representation(output, data, list(final_layers))


if __name__ == "__main__":
    annotate_file()
