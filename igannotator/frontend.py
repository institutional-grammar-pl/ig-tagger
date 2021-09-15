from pathlib import Path

import pandas as pd

from igannotator.backend import (
    get_sentences,
    get_sentence_type,
    get_annotated_sentences
)
from igannotator.output.tsv import write_tsv_representation

sep = '\t'


def set_extension(p: Path) -> Path:
    if not p.suffix:
        return p.with_suffix('.tsv')
    else:
        return p


def atomize(input_path: Path, output_path: Path, sentence_split_type: str = 'rule_based'):
    with open(input_path, 'r') as input_:
        text = input_.read()
    sentences = get_sentences(text, sentence_split_type)

    output_path = set_extension(output_path)
    with open(output_path, 'w+') as output:
        output.write('\n\n'.join(sentences))


def annotate_sentence_type(in_path: Path, out_path: Path):
    with open(in_path, 'r') as input_:
        file_text = input_.read()

    sentences = file_text.split('\n\n')
    df = get_sentence_type(sentences)

    out_path = set_extension(
        Path(out_path)
    )

    df.to_csv(out_path, sep=sep, index=True, index_label='sentence no.')


def annotate_ig(in_path: Path, out_path: Path):
    df = pd.read_csv(in_path, sep=sep, index_col=0)
    annotations = get_annotated_sentences(df)
    out_path = set_extension(out_path)
    write_tsv_representation(out_path, *annotations)



