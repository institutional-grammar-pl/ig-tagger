import click
import warnings
import pathlib

from igannotator.output.mae import write_mae_representation
from igannotator.output.tsv import write_tsv_representation

#from igannotator.annotator import IgAnnotator
from igannotator.annotator.ig_annotator import IgAnnotator

@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
@click.argument("language")
@click.argument("output_format")
@click.argument("type", required=False)

def annotate_file(input, output, language, output_format, type = None):

    with open(input, "r") as f:
        input_text = f.read()
    annotator = IgAnnotator(language, type)
    sentences = [x for x in input_text.split("\n\n") if len(x) > 0]
    data = list()
    connlu_output = 'data/connlu/' + input.split('/')[-1][:-4]+"_connlu.txt"
    connlu_out = open(connlu_output, "w")
    current_component_id = 0
    
    for sentence in sentences:

        connlu_out.write(annotator.get_connlu(sentence))
        connlu_out.write('\n')
        # print('before', '\n\n')
        # print('\n\n\n', annotator.annotate(sentence, current_component_id))
        # print('after', '\n\n')
        tree, tags, current_component_id = annotator.annotate(sentence, current_component_id)
        print('sentence', sentence)
        print('tags', tags)
        data.append((tree, tags))
    connlu_out.close()

    if output_format == 'mae':
        write_mae_representation(output, data)
    elif output_format == 'tsv':
        write_tsv_representation(output, data)

if __name__ == "__main__":
    annotate_file()