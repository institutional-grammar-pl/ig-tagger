from typing import List, Tuple
import re

import pandas as pd

from igannotator.annotator.lexical_tree import LexicalTreeNode
from igannotator.atomic_sentences import (
    filter_sentence,
    gen_atomic_statements,
    nlp
)
from igannotator.rulesexecutor.rules import IGTag

from igannotator.sentence_type import (
    model_pipeline
)

from igannotator.annotations import (
    annotate_sentences
)


def get_sentences(
        txt: str,
        sentence_split_type: str = 'rule_based',
        atomize: bool = True,
        verbose: bool = False
) -> List[str]:
    """
    Split text document into sentences
    :param txt: Text document
    :param sentence_split_type: ml or rule_based - use Spacy or regular expression to split into sentences
    :param atomize: whether try to split enumerations into atomic sentences
    :param verbose: whether create additional output while processing
    :return: list of sentences
    """
    # remove new lines
    txt = re.sub('\n|:|"|;', ' ', txt)
    if sentence_split_type == 'ml':  # split text into sentences by spacy
        doc = nlp(txt)
        sentences = doc.sents
    elif sentence_split_type == 'rule_based':  # split text into sentences using regular expressions
        sentences = re.split(r"([A-Z][^\.!?]*[\.!?])", txt)
    else:
        raise ValueError()

    result = []
    for ind, s in enumerate(sentences):
        if filter_sentence(s):
            curr_sentence = gen_atomic_statements(str(s)) if atomize else str(s)
            if verbose:
                print(f"sentence nr. {ind} ----------\n{curr_sentence}\n-----------------------")
            result.append('\n\n'.join(curr_sentence) if type(curr_sentence) is list else curr_sentence)

    return result


def get_sentence_type(sentences: List[str]) -> pd.DataFrame:
    """
    Assign sentence type
    :param sentences: List of processed and clean sentences
    :return: DataFrame with sentences and their corresponding type (c or r)
    """
    df = pd.DataFrame({
        'text': sentences
    })

    df['sentence_type'] = model_pipeline.predict(df.text)

    df.sentence_type = df.sentence_type.apply(lambda val: 'r' if val else 'c')

    return df


def get_annotated_sentences(sentences: pd.DataFrame) -> Tuple[
    List[Tuple[LexicalTreeNode, List[IGTag]]],
    List[str]
]:
    """

    :param sentences: DataFrame of sentences with sentence type (r/c) - output of get_sentence_type
    :return: Tuple with tagged tokens and used layers
    """
    trees_with_tags = []
    layers = []

    st_groups = sentences.groupby(by='sentence_type')

    for name, group in st_groups:
        st_type = group['sentence_type'][0].lower()
        if st_type == 'r':
            layer_type = 'reg'
        elif st_type == 'c':
            layer_type = 'cons'
        else:
            raise ValueError()

        curr_trees, curr_layers = annotate_sentences(
            list(group['text']),
            language='en', layer=layer_type, conllu_path=False, output_format='tsv', output_path=None)

        trees_with_tags.extend(curr_trees)
        layers.extend(curr_layers)

    return sentences.index, trees_with_tags, layers
