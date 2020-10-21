import click
import warnings

from ..igannotator.output.mae import write_mae_representation
from ..igannotator.output.tsv import write_tsv_representation

from ..igannotator.annotator import IgAnnotator


def annotate_file(input_file, output_file):
    with open(input_file, "r") as f:
        input_text = f.read()

    annotator = IgAnnotator()
    sentences = [x for x in input_text.split("\n\n") if len(x) > 0]

    mae_data = list()
    for sentence in sentences:
        tree, tags = annotator.annotate(sentence)

        mae_data.append((tree, tags))

    write_mae_representation(output_file, mae_data)


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path(exists=False))
def console_entry(input_file, output_file):
    annotate_file(input_file, output_file)


if __name__ == "__main__":
    console_entry()
