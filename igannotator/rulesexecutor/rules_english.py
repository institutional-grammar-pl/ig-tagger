from igannotator.rulesexecutor.rules import *

# 1. Jeżeli jest jeden root to bierzemy go jako:
#    a) jeżeli jest pochodną od słowa móc, musieć, obowiązany to bieżemy go jako deontic
#    b) jeżeli nie jest to bierzemy go jako aIm
class OneRootIsAimOrDeontic(Rule):

    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):

        aux = [n for n in tree.get_all_descendants() if n.relation == "aux"]
        if len(aux) == 1:
            annotations.append(
                IGTag(words=[(aux[0].id, aux[0].value)], tag_name=IGElement.DEONTIC)
            )

        root = [n for n in tree.get_all_descendants() if n.relation == "root"]
        if len(root) == 1:
            annotations.append(
                IGTag(words=[(root[0].id, root[0].value)], tag_name=IGElement.AIM)
            )
            
            


# 3. Jeżeli w poddrzewie aIm jest:
#    - aux:pass - oznacza stronę bierną np. "być przyznane"
#                       - advmod (o polarity:Neg) - zmienia znaczenie słowa (wg dokumentacji), tutaj przeczenie
#    - cop - jest/są np. "są realizowane"
#
# to te części są dodawane do aIm.


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


# 4. Attribute oznaczany jako
#     a) root -> nsubj
# 4. Attribute propery oznaczany jako
#     a) root -> nsubj -> poddrzewa
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

# 5. aIm -> obj + poddrzewa  lub aIm -> iobj + poddrzewa
class ObjsFromAimAreObjects(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):
        
        aim_node = find_node_with_tag(annotations, tree, IGElement.AIM)

        for c in aim_node.children:
            if c.relation == "obj":
                print("obj", c.value, c.get_all_descendants())
                annotations.append(
                    IGTag(
                        words=[(cc.id, cc.value) for cc in c.get_all_descendants()],
                        tag_name=IGElement.OBJECT_DIRECT,
                    )
                )

# 5. aIm -> obj + poddrzewa  lub aIm -> iobj + poddrzewa
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
