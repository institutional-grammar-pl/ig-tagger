from pathlib import Path
import re

import pandas as pd

from igtagger.backend import (
    get_sentences,
    get_sentence_type,
    get_annotated_sentences
)
from igtagger.output.tsv import write_tsv_representation

sep = '\t'


def set_extension(p: Path, ext: str = 'tsv') -> Path:
    if not p.suffix:
        return p.with_suffix('.' + ext)
    else:
        return p


def set_alt_name(p: Path, alt_name):
    return p.parent / (p.stem + '_' + alt_name)


def atomize(input_path: Path, output_path: Path = None,
            sentence_split_type: str = 'rule_based', output_format: str = 'txt'):
    if not output_path:
        output_path = set_alt_name(input_path, 'atomized')

    with open(input_path, 'r') as input_:
        text = input_.read()
    sentences = get_sentences(text, sentence_split_type)

    output_path = set_extension(output_path, output_format)
    if output_format == 'txt':
        with open(output_path, 'w+') as output:
            output.write('\n\n'.join(sentences))
    elif output_format == 'tsv':
        df = pd.DataFrame({
            'text': sentences,
            'sentence_type': [' ' for _ in range(len(sentences))]
        })
        df.index += 1
        df.to_csv(output_path, sep=sep, index=True, index_label='sentence no.')


def annotate_sentence_type(in_path: Path, out_path: Path = None):
    if not out_path:
        out_path = set_alt_name(in_path, 'sen_type')

    if in_path.suffix == '.txt':
        with open(in_path, 'r') as input_:
            file_text = input_.read()
        sentences = file_text.split('\n\n')
    elif in_path.suffix == '.tsv':
        df = pd.read_csv(in_path, sep=sep, index_col=0)
        sentences = df.text
    else:
        return

    sentences = [re.sub(r'\n|\t', ' ', sen) for sen in sentences]
    df = get_sentence_type(sentences)

    out_path = set_extension(
        Path(out_path)
    )

    df.to_csv(out_path, sep=sep, index=True, index_label='sentence no.')


def annotate_ig(in_path: Path, out_path: Path = None):
    if not out_path:
        out_path = set_alt_name(in_path, 'tagged')

    df = pd.read_csv(in_path, sep=sep, index_col=0)
    annotations = get_annotated_sentences(df)
    out_path = set_extension(out_path)
    write_tsv_representation(out_path, *annotations)



