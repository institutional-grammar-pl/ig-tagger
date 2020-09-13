from typing import List

from igannotator.annotator.lexical_tree import LexcialTreeNode
from igannotator.rulesexecutor.rules import IGTag, Rule
from igannotator.rulesexecutor.rules_polish import *
from igannotator.rulesexecutor.rules_english import *

class RulesExecutor:
    def __init__(self, rules: List[Rule]):
        self._rules = rules

    def execute(self, tree: LexcialTreeNode) -> List[IGTag]:
        annotations: List[IGTag] = []
        for r in self._rules:
            r.apply(tree, annotations)
        return [ann for ann in annotations if ann is not None]


class IGRulesExecutor(RulesExecutor):
    def __init__(self, language):

        if language == 'pl': 
            super().__init__(
                [
                    OneRootIsAimOrDeontic(),
                    AimIsXcompFromDeonticRoot(),
                    AimExtension(),
                    NsubjIsAttribute(),
                    ObjsFromAimAreObjects(),
                    PunctFromAimIsSeparator(),
                ]
            )

        elif language == 'en': 
            super().__init__(
                [
                    OneRootIsAimOrDeontic(),
                    AimIsXcompFromDeonticRoot(),
                    AimExtension(),
                    NsubjIsAttribute(),
                    ObjsFromAimAreObjects(),
                    PunctFromAimIsSeparator(),
                ]
            )

