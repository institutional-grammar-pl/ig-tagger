import pandas as pd
from typing import List, Tuple, Optional
import stanfordnlp
import warnings
import numpy as np

from igannotator.annotator.annotator import BaseAnnotator
from igannotator.annotator.lexical_tree import LexcialTreeNode
from igannotator.rulesexecutor.rules import IGTag
from igannotator.annotator.stanford_annotator import StanfordAnnotator
from igannotator.rulesexecutor.rules_executor import IGRulesExecutor

class IgAnnotator(BaseAnnotator):
    def __init__(self, language, type):
        super().__init__()
        self.language = language
        self.type = type

        stanfordnlp.download(
            self.language, self.resources_dir, confirm_if_exists=False, force=True
        )
        self._stanford_annotator = StanfordAnnotator(language = self.language)
        self._executor = IGRulesExecutor(language = self.language, type = self.type)

    def _preprocess(self, sentence):
        def remove_dots(x: str) -> str:
            return x.replace(".", "") + "."

        return remove_dots(sentence)

    def annotate(self, sentence: str, current_component_id) -> Tuple[LexcialTreeNode, List[IGTag]]:
        processed_sentence = self._preprocess(sentence)
        dfs = self._stanford_annotator.annotate(processed_sentence)
        if len(dfs) != 1:
            warnings.warn(f"Unable to annotate data: {sentence}")
            return LexcialTreeNode.from_sentence(sentence), [], current_component_id
        tree = LexcialTreeNode.from_conllu_df(dfs[0])
        tags, current_component_id = self._executor.execute(tree, current_component_id)
        print('annotate_nested')

        nested_tags, current_component_id = self.annotate_nested(tags, current_component_id)
        return tree, tags+nested_tags, current_component_id

    def get_connlu(self, sentence: str) -> str:
        processed_sentence = self._preprocess(sentence)

        doc_response = self._stanford_annotator._annotator(sentence)
        return doc_response.conll_file.conll_as_string()

    def annotate_nested(self, annotations, current_component_id):
        
        ids = np.unique([anno.tag_id for anno in annotations if str(anno.tag_name) in ['IGElement.CONTEXT', 'IGElement.OBJECT_DIRECT']])
        nested_tags = []
        
        for tag_id in ids:
            word_ids = [word[0] for anno in annotations for word in anno.words if anno.tag_id == tag_id]
            sentence = ""
            min_id = min(word_ids)
            max_id = max(word_ids)
            if max_id - min_id >= 3:
                for i in range(min(word_ids), max(word_ids)+1):
                    sentence += [word[1] for anno in annotations for word in anno.words if word[0] == i][0] + " "
                _, tags, current_component_id = self.annotate(sentence, current_component_id)   
                nested_tags += tags

        return nested_tags, current_component_id