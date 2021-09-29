from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from igtagger.rulesexecutor.ig_element import IGElement
from igtagger.annotator.lexical_tree import LexicalTreeNode


@dataclass
class IGTag:
    word_id: int
    word: str
    tag_name: IGElement
    tag_id: int
    level_id: int
    layer: str


class Rule(ABC):
    @abstractmethod
    def apply(self, tree: LexicalTreeNode, annotations: List[IGTag]):
        raise NotImplementedError()


def find_word_tag(annotations: List[IGTag], word_id: str, layer=None) -> Optional[IGTag]:
    result = []
    for ann in annotations:
        if int(ann.word_id) == int(word_id):
            result.append(ann)
    if layer is None:
        return result
    else:
        return {l: [ann for ann in result if ann.layer == l] for l in layer}


def find_by_word_id(annotations: List[IGTag], word_id: int, level_id):
    tag = [anno for anno in annotations if anno.word_id == word_id and anno.level_id == level_id]
    if len(tag) != 0:
        return tag[0]
    else:
        return tag
