from igannotator.rulesexecutor.rules import Rule, IGTag
from typing import List
from igannotator.rulesexecutor.ig_element import IGElement
from igannotator.annotator.lexical_tree import LexicalTreeNode


class Aim(Rule):
    def apply(self, tree: LexicalTreeNode, annotations: List[IGTag], component_id, level_id):
        root = [n for n in tree.get_all_descendants() if n.relation == "root"]
        if len(root) == 1:
            annotations.append(
                IGTag(word_id=root[0].id, word=root[0].value, tag_name=IGElement.AIM, tag_id=None, level_id=level_id, layer='reg')
            )
            for c in root[0].children:
                if (c.relation in ["aux:pass", "cop"]) or (c.relation == "aux" and c.lemm in ["be", "have", "do"]) or (c.relation == "advmod" and c.lemm == "not"):
                    annotations.append(
                        IGTag(word_id=c.id, word=c.value, tag_name=IGElement.AIM, tag_id=None, level_id=level_id, layer='reg')
                    )
        else:
            return -1
        return component_id


class Deontic(Rule):
    def apply(self, tree: LexicalTreeNode, annotations: List[IGTag], component_id, level_id):
        root = [n for n in tree.get_all_descendants() if n.relation == "root"]
        if len(root) == 1:
            aux = [n for n in root[0].children if n.relation == "aux" and n.lemm in ["must", "should", "may", "might", "can", "could", "need", "ought", "shall"]]
            if len(aux) == 1:
                annotations.append(
                    IGTag(word_id=aux[0].id, word=aux[0].value, tag_name=IGElement.DEONTIC, tag_id=None, level_id=level_id, layer='reg')
                )
        return component_id


class Attribute(Rule):
    def apply(self, tree: LexicalTreeNode, annotations: List[IGTag], component_id, level_id):
        attribute_found = 0
        for c in tree.children:
            attribute, attribute_prop = 0, 0
            if c.relation in ["nsubj", "nsubj:pass"]:
                for cc in c.get_all_descendants():
                    if cc == c or (cc.relation == "det" and cc.parent == c.id):
                        attribute = 1
                        annotations.append(
                            IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.ATTRIBUTE, tag_id=component_id, level_id=level_id, layer='reg')
                        )
                    else:
                        attribute_prop = 1
                        annotations.append(
                            IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.ATTRIBUTE_PROPERTY, tag_id=component_id + 1, level_id=level_id, layer='reg')
                        )
                component_id += attribute + attribute_prop
                attribute_found = 1

            elif c.relation == "conj":
                for cc in c.get_all_descendants():
                    if cc.relation != "cc":
                        annotations.append(
                            IGTag(
                                word_id=cc.id, word=cc.value,
                                tag_name=IGElement.ATTRIBUTE_PROPERTY, tag_id=component_id,
                                level_id=level_id, layer='reg'
                            )
                        )
                component_id += 1
                attribute_found = 1

        if attribute_found == 0:
            return -1

        return component_id


class Object_Context(Rule):
    def apply(self, tree: LexicalTreeNode, annotations: List[IGTag], component_id, level_id):

        for c in tree.children:

            object_direct, object_direct_prop = 0, 0
            if c.relation == "obj":
                print("obj", c)
                annotations.append(
                    IGTag(
                        word_id=c.id, word=c.value,
                        tag_name=IGElement.OBJECT, tag_id=component_id, level_id=level_id, layer='reg'
                    )
                )

                for cc in c.children:

                    if cc.relation == "advcl" and cc.parent == c.id:
                        for ccc in cc.get_all_descendants():
                            annotations.append(
                                IGTag(
                                    word_id=ccc.id, word=ccc.value,
                                    tag_name=IGElement.CONTEXT, tag_id=component_id, level_id=level_id, layer='reg'
                                )
                            )
                        component_id += 1

                    elif cc.relation in ["det", "amod", "case", "compound"]:
                        object_direct = 1
                        annotations.append(
                            IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.OBJECT, tag_id=component_id, level_id=level_id, layer='reg')
                        )
                        for ccc in cc.get_all_descendants():
                            annotations.append(
                                IGTag(word_id=ccc.id, word=ccc.value, tag_name=IGElement.OBJECT_PROPERTY, tag_id=component_id, level_id=level_id, layer='reg')
                            )

                    elif cc.relation in ["nmod", "nmod:poss"]:
                        object_direct = 1
                        annotations.append(
                            IGTag(word_id=cc.id, word=cc.value, tag_name=IGElement.OBJECT, tag_id=component_id, level_id=level_id, layer='reg')
                        )
                        for ccc in cc.get_all_descendants():
                            if (ccc.relation in ["case", "amod"] and ccc.parent == cc.id):
                                print("obj nmod", ccc.relation, ccc.value)
                                annotations.append(
                                    IGTag(word_id=ccc.id, word=ccc.value, tag_name=IGElement.OBJECT, tag_id=component_id, level_id=level_id, layer='reg')
                                )
                            else:
                                annotations.append(
                                    IGTag(word_id=ccc.id, word=ccc.value, tag_name=IGElement.OBJECT_PROPERTY, tag_id=component_id, level_id=level_id, layer='reg')
                                )

                    else:
                        for ccc in cc.get_all_descendants():
                            annotations.append(
                                    IGTag(
                                        word_id=ccc.id, word=ccc.value, tag_name=IGElement.OBJECT_PROPERTY,
                                        tag_id=component_id + 1, level_id=level_id, layer='reg'
                                    )
                                )
                component_id += object_direct + object_direct_prop

            elif c.relation in ["advcl", "obl"] or (c.relation == "advmod" and c.lemm != "not"):
                for cc in c.get_all_descendants():
                    annotations.append(
                        IGTag(
                            word_id=cc.id, word=cc.value,
                            tag_name=IGElement.CONTEXT, tag_id=component_id, level_id=level_id, layer='reg')
                    )
                component_id += 1
            elif c.relation == "ccomp":
                that = [cc for cc in c.children if cc.value == 'that' and cc.relation == 'mark']
                if len(that) != 0:
                    for cc in c.get_all_descendants():
                        annotations.append(
                            IGTag(
                                word_id=cc.id, word=cc.value,
                                tag_name=IGElement.OBJECT, tag_id=component_id, level_id=level_id, layer='reg')
                        )
                else:
                    for cc in c.get_all_descendants():
                        annotations.append(
                            IGTag(
                                word_id=cc.id, word=cc.value,
                                tag_name=IGElement.CONTEXT, tag_id=component_id, level_id=level_id, layer='reg')
                        )

            elif c.relation == "xcomp":
                for cc in c.children:
                    if cc.relation == "obj":
                        annotations.append(
                            IGTag(
                                word_id=cc.id, word=cc.value,
                                tag_name=IGElement.OBJECT, tag_id=component_id+1, level_id=level_id, layer='reg'
                            )
                        )
                        for ccc in cc.get_all_descendants():
                            if ccc != cc:
                                annotations.append(
                                    IGTag(
                                        word_id=ccc.id, word=ccc.value,
                                        tag_name=IGElement.OBJECT_PROPERTY, tag_id=component_id+1, level_id=level_id, layer='reg'
                                    )
                                )
                    else:
                        for ccc in cc.get_all_descendants():
                            annotations.append(
                                IGTag(
                                    word_id=ccc.id, word=ccc.value,
                                    tag_name=IGElement.CONTEXT, tag_id=component_id, level_id=level_id, layer='reg'
                                )
                            )
                component_id += 2

        return component_id
