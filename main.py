import click
from igannotator.output.tsv import write_tsv_representation
from igannotator.annotator.ig_annotator import IgAnnotator
import re

def preprocess_text(text):
    text = re.sub('[\.] (?=[A-Z])', '.\n', text)
    text = re.sub('\t', ' ', text)
    text = re.sub('["|”|„|“]', '', text)
    text = re.sub("'", '', text)
    text = re.sub('\n[\d]+[. ]', "\n", text)
    text = re.sub("\n(\s*\n){0,1}", "\n\n", text)
    text = re.sub('[ ]+', ' ', text)
    return text

def split_text(text):
    sentences = text.split('\n\n')
    sentences = [text.strip() for text in sentences]
    sentences = [text for text in sentences if text != '']
    return sentences

def annotate_sentences(sentences, output_path, language, output_format, layer, conllu_path):

    if language != "en":
        exit('Unsopperted language. At the moment only annotations of english text are supported.')
    if output_format != "tsv":
        exit('Unsopperted output format. At the moment output to tsv file is supported.')
    if layer not in ['reg', 'cons', 'both']:
        exit('Unsopperted layer type. At the moment only "reg", "cons", "both" values are supported')

    if layer in ['reg', 'cons']:
        layers = [layer]
    else:
        layers = ['reg', 'cons']

    annotator = IgAnnotator(language, layers)
    data = list()
    current_component_id = 1
    level_id = 1

    if conllu_path:
        connlu_out = open(conllu_path, "w")

    final_layers = set()
    for sentence in sentences:
        if conllu_path:
            connlu_out.write(annotator.get_connlu_sentence(sentence))
            connlu_out.write('\n')
        tree, tags, current_component_id, used_layers = annotator.annotate_sentence(sentence, current_component_id, level_id, layers)
        data.append((sentence, tree, tags))
        final_layers.update(used_layers)

    if conllu_path:
        connlu_out.close()

    if output_format == 'tsv':
        write_tsv_representation(output_path, data, list(final_layers))


def annotate_text(text, output_path, language, output_format, layer, conllu_path):

    text = preprocess_text(text)
    sentences = split_text(text)
    annotate_sentences(sentences, output_path, language, output_format, layer, conllu_path)


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
@click.argument("layer", required=False, default="both")
#@click.argument("language", default="en", required=False)
#@click.argument("output_format", default="tsv", required=False)
@click.argument("conllu_path", default=False, required=False)
def annotate_file(input, output, layer, conllu_path):

    with open(input, "r") as f:
        input_text = f.read()
    sentences = [x for x in input_text.split("\n\n") if len(x) > 0]
    annotate_sentences(sentences, output, 'en', 'tsv', layer, conllu_path)


if __name__ == "__main__":
    annotate_file()
