from ...igannotator.rulesexecutor.rules import *

# 1. Jeżeli jest jeden root to bierzemy go jako:
#    a) jeżeli jest pochodną od słowa móc, musieć, obowiązany to bieżemy go jako deontic
#    b) jeżeli nie jest to bierzemy go jako aIm
class OneRootIsAimOrDeontic(Rule):

    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):

        if len([n for n in tree.get_all_descendants() if n.relation == "root"]) != 1:
            return

        if tree.lemm in ["musieć", "móc", "obowiązany"]:
            annotations.append(
                IGTag(words=[(tree.id, tree.value)], tag_name=IGElement.DEONTIC)
            )
        else:
            annotations.append(
                IGTag(words=[(tree.id, tree.value)], tag_name=IGElement.AIM)
            )

# 2. Jeżeli korzeniem jest deontic to aIm jest root -> xcomp
class AimIsXcompFromDeonticRoot(Rule):

    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):

        if (
            tree.relation == "root"
            and find_word_igelement(annotations, tree.id) == IGElement.DEONTIC
        ):
            for c in tree.children:
                if c.relation == "xcomp":
                    annotations.append(
                        IGTag(words=[(c.id, c.value)], tag_name=IGElement.AIM)
                    )


# 3. Jeżeli w poddrzewie aIm jest:
#    - expl:pv - oznacza "się"
#    - aux:pass - oznacza stronę bierną np. "być przyznane"
#    - advmod o polarity:Neg - zmienia znaczenie słowa (wg dokumentacji), tutaj przeczenie
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
            if c.relation in ["expl:pv", "aux:pass", "cop"]:
                aim_tag.words.append((c.id, c.value))
            if c.relation == "advmod" and c.polarity == "Polarity=Neg":
                aim_tag.words.append((c.id, c.value))


# 4. Attribute oznaczany jako:
#     a) root -> nsubj + poddrzewa
#     b) jeżeli od root nie odchodzi nsubj to bierzemy root -> advcl + poddrzewa (jeden przykład gs 24)
class NsubjIsAttribute(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):
        found_nsubj = False
        for c in tree.children:
            if c.relation == "nsubj":
                found_nsubj = True
                annotations.append(
                    IGTag(
                        words=[(cc.id, cc.value) for cc in c.get_all_descendants()],
                        tag_name=IGElement.ATTRIBUTE,
                    )
                )

        if not found_nsubj:
            for c in tree.children:
                if c.relation == "advcl":
                    annotations.append(
                        IGTag(
                            words=[(cc.id, cc.value) for cc in c.get_all_descendants()],
                            tag_name=IGElement.ATTRIBUTE,
                        )
                    )


# TODO:
# 5. oBject i aCtor:
#     a) aIm -> obj + poddrzewa  lub aIm -> iobj + poddrzewa
class ObjsFromAimAreObjects(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag]):
        if find_word_igelement(annotations, tree.id) != IGElement.AIM:
            return

        for c in tree.children:
            if c.relation in ["obj", "iobl"]:
                noun_type = nounClassifier(c.lemm)
                if noun_type is not None:
                    annotations.append(
                        IGTag(
                            words=[(cc.id, cc.value) for cc in c.get_all_descendants()],
                            tag_name=noun_type,
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
