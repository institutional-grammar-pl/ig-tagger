from typing import List, Tuple
from io import StringIO
import tempfile
from stanza.utils.conll import CoNLL
import stanza as stanfordnlp
import warnings
import numpy as np

from igtagger.annotator.annotator import BaseAnnotator
from igtagger.annotator.lexical_tree import LexicalTreeNode
from igtagger.rulesexecutor.rules import IGTag
from igtagger.annotator.stanford_annotator import StanfordAnnotator
from igtagger.rulesexecutor.rules_executor import IGRulesExecutor


class IgAnnotator(BaseAnnotator):

    def __init__(self, language, layers):
        super().__init__()
        self.language = language
        self.layers = layers
        stanfordnlp.download('en')
        stanfordnlp.download(
            self.language, self.resources_dir
        )

        self._stanford_annotator = StanfordAnnotator(language=self.language)
        self._executor = {}

        for layer in self.layers:
            self._executor[layer] = IGRulesExecutor(language=self.language, layer=layer)

    def _preprocess(self, sentence: str) -> str:
        def remove_dots(x: str) -> str:
            return x.replace(".", "") + "."

        return remove_dots(sentence)

    def annotate_sentence(self, sentence: str, current_component_id, depth, layers) -> \
            Tuple[LexicalTreeNode, List[IGTag], int, List[str]]:
        processed_sentence = self._preprocess(sentence)
        dfs = self._stanford_annotator.annotate(processed_sentence)
        if len(dfs) == 0:
            warnings.warn(f"Unable to annotate data: {sentence}")
            return LexicalTreeNode.from_sentence(sentence), [], current_component_id, []
        tree = LexicalTreeNode.from_conllu_df(dfs[0])
        tags_all = []
        used_layers = []
        for layer in layers:
            tags, current_component_id = self._executor[layer].execute(tree, current_component_id, depth)
            if tags:
                tags_all += tags
                used_layers.append(layer)

            nested_tags, current_component_id = self.annotate_nested_statement(tags_all, tree, current_component_id,
                                                                               depth + 1, layer)
            tags_all += nested_tags
        return tree, tags_all, current_component_id, used_layers

    def get_connlu_sentence(self, sentence: str) -> str:
        processed_sentence = self._preprocess(sentence)

        doc_response = self._stanford_annotator._annotator(processed_sentence)
        fp, tmp = tempfile.mkstemp()
        CoNLL.write_doc2conll(doc_response, tmp)
        with open(tmp, encoding='utf-8') as f:
            conll_string = f.read()
        return conll_string

    def annotate_nested_statement(self, annotations, tree, current_component_id, depth, layer):
        if layer == 'reg':
            ids = np.unique(
                [anno.tag_id for anno in annotations if str(anno.tag_name) in ['IGElement.CONTEXT', 'IGElement.OBJECT',
                                                                               'IGElement.ATTRIBUTE',
                                                                               'IGElement.ATTRIBUTE_PROPERTY',
                                                                               'IGElement.OBJECT_PROPERTY']])
        elif layer == 'cons':
            ids = np.unique(
                [anno.tag_id for
                 anno in annotations if
                 str(anno.tag_name) in ['IGElement.CONSTITUTIVE_FUNCTION',
                                        'IGElement.CONSTITUTING_PROPERTIES',
                                        'IGElement.CONSTITUTED_ENTITY',
                                        'IGElement.CONSTITUTED_ENTITY_PROPERTY',
                                        'IGElement.CONTEXT',
                                        'IGElement.MODAL']
                 and anno.tag_id is not None
                 ])

        else:
            return [], current_component_id
        nested_tags = []

        if depth > 1:
            return nested_tags, current_component_id
        sent = [x.value for x in tree.get_all_descendants()]
        for tag_id in ids:
            word_ids = [anno.word_id for anno in annotations if anno.tag_id == tag_id]
            sentence = ""
            min_id = min(word_ids)
            max_id = max(word_ids)
            if max_id - min_id >= 5:

                sentence += ' '.join(sent[min_id:max_id])

                _, tags, current_component_id, _ = self.annotate_sentence(sentence, current_component_id, depth,
                                                                          [layer])

                correct_tags = []
                for tag in tags:
                    x = tag
                    x.word_id += min_id
                    correct_tags.append(x)
                nested_tags += correct_tags

        return nested_tags, current_component_id
