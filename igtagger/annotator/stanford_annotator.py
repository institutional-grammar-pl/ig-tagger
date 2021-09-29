import pandas as pd
import stanza as stanfordnlp
from stanza.utils.conll import CoNLL
from io import StringIO
import tempfile

from igtagger.annotator.annotator import BaseAnnotator


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
        fp, tmp = tempfile.mkstemp()
        CoNLL.write_doc2conll(doc_response, tmp)
        with open(tmp, encoding='utf-8') as f:
            conll_string = f.read()
        return [
            self._sentence_to_df(sentence)
            for sentence in conll_string.split("\n\n")
            if len(sentence) > 0
        ]
