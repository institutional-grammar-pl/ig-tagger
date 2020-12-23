from typing import List
import igannotator.rulesexecutor.rules_polish as rules_pl
import igannotator.rulesexecutor.rules_english as rules_en
import igannotator.rulesexecutor.rules_english_constitutive as rules_en_cons 
import igannotator.rulesexecutor.rules_english_regulative as rules_en_reg

from igannotator.rulesexecutor.rules import IGTag, Rule
from igannotator.annotator.lexical_tree import LexcialTreeNode


class RulesExecutor:
    def __init__(self, rules: List[Rule]):
        self._rules = rules

    def execute(self, tree: LexcialTreeNode, current_component_id) -> List[IGTag]:
        annotations: List[IGTag] = []
        component_id = current_component_id
        for r in self._rules:
            component_id = r.apply(tree, annotations, component_id)
        annotations = [ann for ann in annotations if ann is not None]

        return annotations, component_id

class IGRulesExecutor(RulesExecutor):
    def __init__(self, language, type):

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
            if type == None: 
                print('None')
                super().__init__(
                    [
                        rules_en.Aim(),
                        rules_en.AuxilaryVerbs(),
                        rules_en.AimExtension(),
                        rules_en.Attribute(),
                        rules_en.Context(),
                        rules_en.Objects(),
                        rules_en.Separator(),
                    ]
                )
            elif type == 'reg':
                print('reg')
                super().__init__(
                    [
                        rules_en_reg.Aim(),
                        rules_en_reg.AuxilaryVerbs(),
                        rules_en_reg.AimExtension(),
                        rules_en_reg.Attribute(),
                        rules_en_reg.Context(),
                        rules_en_reg.Objects(),
                        rules_en_reg.Separator(),
                    ]
                )   
            elif type == 'cons':
                print('cons') 
                super().__init__(
                    [
                        rules_en_cons.ConstitutiveRules()
                    ]
                )  
            else:
                print('other') 

