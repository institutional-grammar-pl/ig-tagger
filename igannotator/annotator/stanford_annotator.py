import pandas as pd
import stanfordnlp
from io import StringIO

from igannotator.annotator.annotator import BaseAnnotator

class StanfordAnnotator(BaseAnnotator):
    def __init__(self, language):
        super().__init__()
        self.language = language
        self._annotator = stanfordnlp.Pipeline(**self._get_config())

    def _get_config(self):
        return {
            "models_dir": self.resources_dir,
            "processors": "tokenize,pos,lemma,depparse",
            "lang": self.language,
        }

    def _sentence_to_df(self, sentence: str):
        # CoNLL-U https://universaldependencies.org/format.html
        cols = [
            "id",
            "form",
            "lemma",
            "upos",
            "xpos",
            "feats",
            "head",
            "deprel",
            "deps",
            "misc",
        ]
        return pd.read_csv(StringIO(sentence), sep="\t", header=None, names=cols)

    def annotate(self, text: str):
        doc_response = self._annotator(text)
        conll_string = doc_response.conll_file.conll_as_string()
        return [
            self._sentence_to_df(sentence)
            for sentence in conll_string.split("\n\n")
            if len(sentence) > 0
        ]
