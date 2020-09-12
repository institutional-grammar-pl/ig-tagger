import click
import warnings
import pathlib

from igannotator.output.mae import write_mae_representation
from igannotator.annotator import IgAnnotator

@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
@click.argument("language")

def annotate_file(input, output, language):

    with open(input, "r") as f:
        input_text = f.read()

    annotator = IgAnnotator(language)
    sentences = [x for x in input_text.split("\n\n") if len(x) > 0]

    mae_data = list()
    connlu_output = input.split('.')[0]+"_connlu.txt"
    connlu_out = open(connlu_output, "w")

    for sentence in sentences:

        connlu_out.write(annotator.get_connlu(sentence))
        connlu_out.write('\n')

        tree, tags = annotator.annotate(sentence)
        mae_data.append((tree, tags))
    connlu_out.close()
    write_mae_representation(output, mae_data)

if __name__ == "__main__":
    annotate_file()

