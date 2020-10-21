from ...igannotator.rulesexecutor.rules import *

class OneRootIsAim(Rule):

    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):

        root = [n for n in tree.get_all_descendants() if n.relation == "root"]
        if len(root) == 1:
            annotations.append(
                IGTag(words=[(root[0].id, root[0].value)], tag_name=IGElement.AIM)
            )


class AuxilaryVerbs(Rule):

    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):

        root = [n for n in tree.get_all_descendants() if n.relation == "root"]
        
        if len(root) == 1:
            aux = [n for n in root[0].children if n.relation == "aux" and n.lemm in ["must", "should", "may", "might", "can", "could", "need", "ought", "shall"]]
            if len(aux) == 1:
                annotations.append(
                    IGTag(words=[(aux[0].id, aux[0].value)], tag_name=IGElement.DEONTIC)
                )
            aux_do = [n for n in root[0].children if n.relation == "aux" and n.lemm == "do"]
            if len(aux_do) == 1:
                annotations.append(
                    IGTag(words=[(aux_do[0].id, aux_do[0].value)], tag_name=IGElement.AIM)
                )


class AimExtension(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):
        aim_node = find_node_with_tag(annotations, tree, IGElement.AIM)

        if aim_node is None:
            return

        aim_tag = find_word_tag(annotations, aim_node.id)

        for c in aim_node.children:
            if c.relation in ["aux:pass", "cop"]:
                aim_tag.words.append((c.id, c.value))
            if c.relation == "advmod" and c.lemm == "not":
                aim_tag.words.append((c.id, c.value))

class NsubjIsAttribute(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):
        found_nsubj = False
        for c in tree.children:
            if c.relation in ["nsubj", "nsubj:pass"]:
                annotations.append(
                    IGTag(
                        words=[(c.id, c.value)],
                        tag_name=IGElement.ATTRIBUTE,
                    )
                )
                annotations.append(
                    IGTag(
                        words=[(cc.id, cc.value) for cc in c.get_all_descendants() if cc != c],
                        tag_name=IGElement.ATTRIBUTE_PROPERTY,
                    )
                )

class ObjsFromAimAreObjects(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):
        
        aim_node = find_node_with_tag(annotations, tree, IGElement.AIM)

        for c in aim_node.children:
            if c.relation == "obj":
                #print("obj", c.value, c.get_all_descendants())
                annotations.append(
                    IGTag(
                        words=[(cc.id, cc.value) for cc in c.get_all_descendants()],
                        tag_name=IGElement.OBJECT_DIRECT,
                    )
                )

class Context(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):
        
        aim_node = find_node_with_tag(annotations, tree, IGElement.AIM)

        for c in aim_node.children:
            if c.relation == "adv":
                annotations.append(
                    IGTag(
                        words=[(c.id, c.value)],
                        tag_name=IGElement.EXEC_CONSTRAINT,
                    )
                )
            elif c.relation == "obl":
                annotations.append(
                    IGTag(
                        words=[(cc.id, cc.value) for cc in c.get_all_descendants()],
                        tag_name=IGElement.EXEC_CONSTRAINT,
                    )
                )

class PunctFromAimIsSeparator(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):
        if find_word_igelement(annotations, tree.id) != IGElement.AIM:
            return

        for c in tree.children:
            if c.relation == "punct":
                annotations.append(
                    IGTag(words=[(c.id, c.value)], tag_name=IGElement.SEPARATOR)
                )
