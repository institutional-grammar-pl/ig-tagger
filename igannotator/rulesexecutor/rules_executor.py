from typing import List

from igannotator.annotator.lexical_tree import LexcialTreeNode
from igannotator.rulesexecutor.rules import IGTag, Rule
import igannotator.rulesexecutor.rules_polish as rules_pl
import igannotator.rulesexecutor.rules_english as rules_en

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
                    rules_pl.OneRootIsAimOrDeontic(),
                    rules_pl.AimIsXcompFromDeonticRoot(),
                    rules_pl.AimExtension(),
                    rules_pl.NsubjIsAttribute(),
                    rules_pl.ObjsFromAimAreObjects(),
                    rules_pl.PunctFromAimIsSeparator(),
                ]
            )

        elif language == 'en': 
            super().__init__(
                [
                    rules_en.OneRootIsAim(),
                    rules_en.AuxilaryVerbs(),
                    rules_en.AimExtension(),
                    rules_en.NsubjIsAttribute(),
                    rules_en.ObjsFromAimAreObjects(),
                    rules_en.Context(),
                    rules_en.PunctFromAimIsSeparator(),
                ]
            )