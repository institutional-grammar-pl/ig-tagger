from typing import List
import igannotator.rulesexecutor.rules_english_constitutive as rules_en_cons
import igannotator.rulesexecutor.rules_english_regulative as rules_en_reg

from igannotator.rulesexecutor.rules import IGTag, Rule
from igannotator.annotator.lexical_tree import LexicalTreeNode


class RulesExecutor:
    def __init__(self, rules: List[Rule]):
        self._rules = rules

    def execute(self, tree: LexicalTreeNode, current_component_id, level_id) -> List[IGTag]:
        annotations: List[IGTag] = []
        component_id = current_component_id
        for r in self._rules:
            component_id = r.apply(tree, annotations, component_id, level_id)
            if component_id == -1:
                return [], current_component_id
        annotations = [ann for ann in annotations if ann is not None]
        return annotations, component_id


class IGRulesExecutor(RulesExecutor):
    def __init__(self, language, layer):

        if language == 'en':
            if layer == 'reg':
                super().__init__(
                    [
                        rules_en_reg.Aim(),
                        rules_en_reg.Deontic(),
                        rules_en_reg.Attribute(),
                        rules_en_reg.Object_Context(),
                    ]
                )
            elif layer == 'cons':
                super().__init__(
                    [
                        rules_en_cons.ConstitutiveRules()
                    ]
                )

            else:
                print('other')
