import click
import warnings
import pathlib
import tempfile

from .igannotator.output.mae import write_mae_representation
from .igannotator.output.tsv import write_tsv_representation

from .igannotator.annotator import IgAnnotator


def annotate_text(sentences, output_path, language, output_format):
    annotator = IgAnnotator(language)
    conllu_file = tempfile.NamedTemporaryFile()
    data = list()
    with open(conllu_file.name) as conllu_out:
        for sentence in sentences:
            conllu_out.write(annotator.get_connlu(sentence))
            conllu_out.write('\n')

            tree, tags = annotator.annotate(sentence)
            data.append((tree, tags))

        if output_format == 'mae':
            write_mae_representation(output_path, data)
        elif output_format == 'tsv':
            write_tsv_representation(output_path, data)


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
@click.argument("language")
@click.argument("output_format")
def annotate_file(input_, output, language, output_format):
    with open(input_, "r") as f:
        input_text = f.read()
    sentences = [x for x in input_text.split("\n\n") if len(x) > 0]
    output = pathlib.Path(output) / pathlib.Path(input_).stem + '_an.' + output_format
    annotate_text(sentences, output, language, output_format)


if __name__ == "__main__":
    annotate_file()
