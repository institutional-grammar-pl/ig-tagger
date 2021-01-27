from igannotator.rulesexecutor.rules import Rule, IGTag
from typing import List
from igannotator.rulesexecutor.ig_element import IGElement
from igannotator.annotator.lexical_tree import LexicalTreeNode


class ConstitutiveRules(Rule):

    def apply(self, tree: LexicalTreeNode, annotations: List[IGTag], component_id, level_id):

        root = [n for n in tree.get_all_descendants() if n.relation == "root"]
        if len(root) == 1:

            if root[0].tag == 'VERB' or root[0].tag == 'ADJ':

                if root[0].tag == 'ADJ':
                    annotations.append(
                        IGTag(
                            word_id=root[0].id, word=root[0].value,
                            tag_name=IGElement.CONSTITUTING_PROPERTIES, tag_id=None,
                            level_id=level_id, layer='cons')
                    )
                else:
                    annotations.append(
                        IGTag(
                            word_id=root[0].id, word=root[0].value,
                            tag_name=IGElement.CONSTITUTIVE_FUNCTION, tag_id=None,
                            level_id=level_id, layer='cons')
                    )

                for c in root[0].children:
                    if (c.relation in ["aux:pass", "cop"]) or (c.relation == "aux" and c.lemm in ["be", "have", "do"]) or (c.relation == "advmod" and c.lemm == "not"):
                        annotations.append(
                            IGTag(word_id=c.id, word=c.value, tag_name=IGElement.CONSTITUTIVE_FUNCTION, tag_id=None, level_id=level_id, layer='cons')
                        )

                entities = [c for c in root[0].children if c.relation in ["nsubj", "nsubj:pass", "expl"]]
                if entities == []:
                    return -1
                for c in entities:
                    annotations.append(
                            IGTag(word_id=c.id, word=c.value, tag_name=IGElement.CONSTITUTED_ENTITY, tag_id=component_id, level_id=level_id, layer='cons')
                        )
                    for cc in c.children:
                        if cc.relation in ["det", "compound", "mark"]:
                            for ccc in cc.get_all_descendants():
                                annotations.append(
                                    IGTag(word_id=ccc.id, word=ccc.value, tag_name=IGElement.CONSTITUTED_ENTITY, tag_id=component_id, level_id=level_id, layer='cons')
                                )
                        else:
                            for ccc in cc.get_all_descendants():
                                annotations.append(
                                    IGTag(word_id=ccc.id, word=ccc.value, tag_name=IGElement.CONSTITUTED_ENTITY_PROPERTY, tag_id=component_id, level_id=level_id, layer='cons')
                                )                            
                    component_id += 1

                properties = [c for c in root[0].children if c.relation in ["obl", "obj", "advcl"]]
                for c in properties:
                    for cc in c.get_all_descendants():
                        annotations.append(
                            IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.CONSTITUTING_PROPERTIES, tag_id=component_id, level_id=level_id, layer='cons')
                        )
                    component_id += 1

                context = [c for c in root[0].children if c.relation in ["advmod", "xcomp"]]
                for c in context:
                    for cc in c.get_all_descendants():
                        annotations.append(
                            IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.CONTEXT, tag_id=component_id, level_id=level_id, layer='cons')
                        )
                    component_id += 1

            elif root[0].tag == 'NOUN':

                csubj = [c for c in root[0].children if c.relation == "csubj"]
                cop = [n for n in root[0].children if n.relation == "cop"]
                if len(csubj) == 1:
                    annotations.append(
                        IGTag(word_id=csubj[0].id, word=csubj[0].value, tag_name=IGElement.CONSTITUTIVE_FUNCTION, tag_id=None, level_id=level_id, layer='cons')
                    )

                    csubj_obl = [c for c in csubj[0].children if c.relation == "obl"]
                    for c in csubj_obl:
                        for cc in c.get_all_descendants():
                            annotations.append(
                                IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.CONTEXT, tag_id=component_id, level_id=level_id, layer='cons')
                            )
                        component_id += 1
                    for c in cop:
                        for cc in c.get_all_descendants():
                            annotations.append(
                                IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.CONSTITUTED_ENTITY, tag_id=None, level_id=level_id, layer='cons')
                            )
                else:
                    cop = [n for n in root[0].children if n.relation == "cop"]
                    if cop == []:
                        return -1
                    elif len(cop) == 1:
                        annotations.append(
                            IGTag(word_id=cop[0].id, word=cop[0].value, tag_name=IGElement.CONSTITUTIVE_FUNCTION, tag_id=None, level_id=level_id, layer='cons')
                        )

                entities = [c for c in root[0].children if c.relation in ["det", "acl", "nmod:npmod"]]
                if entities == []:
                    return -1
                annotations.append(
                    IGTag(word_id=root[0].id, word=root[0].value, tag_name=IGElement.CONSTITUTED_ENTITY, tag_id=None, level_id=level_id, layer='cons')
                )
                for c in entities:
                    for cc in c.get_all_descendants():
                        if (cc == c) or (cc.parent == cc.id and cc.relation in ["det", "mark"]):
                            annotations.append(
                               IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.CONSTITUTED_ENTITY, tag_id=component_id, level_id=level_id, layer='cons')
                            )
                        else:
                            annotations.append(
                               IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.CONSTITUTED_ENTITY_PROPERTY, tag_id=component_id, level_id=level_id, layer='cons')
                            )
                    component_id += 1

                properties = [c for c in root[0].children if c.relation in ["nsubj", "nsubj:pass"]]
                for c in properties:
                    for cc in c.get_all_descendants():
                        annotations.append(
                            IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.CONSTITUTING_PROPERTIES, tag_id=component_id, level_id=level_id, layer='cons')
                        )
                    component_id += 1

            aux = [c for c in root[0].children if c.relation == "aux" and c.lemm in ["must", "should", "may", "might", "can", "could", "need", "ought", "shall"]]
            if len(aux) == 1:
                annotations.append(
                    IGTag(word_id=aux[0].id, word=aux[0].value, tag_name=IGElement.MODAL, tag_id=None, level_id=level_id, layer='cons')
                )
        return component_id
