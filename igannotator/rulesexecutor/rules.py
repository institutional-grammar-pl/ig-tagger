from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from dataclasses import dataclass

from ...igannotator.annotator.lexical_tree import LexcialTreeNode
from ...igannotator.rulesexecutor.noun_classifier import nounClassifier
from ...igannotator.rulesexecutor.ig_element import IGElement


@dataclass
class IGTag:
    words: List[Tuple[str, str]]
    tag_name: IGElement


class Rule(ABC):
    @abstractmethod
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):
        raise NotImplementedError()


def find_word_tag(annotations: List[IGTag], word_id: str) -> Optional[IGTag]:
    for ann in annotations:
        for id, word in ann.words:
            if int(id) == int(word_id):
                return ann

    return None

def find_node_with_tag(
    annotations: List[IGTag], tree: LexcialTreeNode, ig: IGElement
) -> Optional[LexcialTreeNode]:
    for t in tree.get_all_descendants():
        if find_word_igelement(annotations, t.id) == ig:
            return t
    return None


def find_word_igelement(annotations: List[IGTag], word_id: str) -> IGElement:
    tag = find_word_tag(annotations, word_id)
    if tag is not None:
        return tag.tag_name
    else:
        return None


