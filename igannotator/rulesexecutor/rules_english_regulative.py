from igannotator.rulesexecutor.rules import *

class Aim(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag], component_id):
        root = [n for n in tree.get_all_descendants() if n.relation == "root"]

        if len(root) == 1:
            annotations.append(
                IGTag(words=[(root[0].id, root[0].value)], tag_name=IGElement.AIM, tag_id=None)
            )
        return component_id

class AuxilaryVerbs(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag], component_id):
        root = [n for n in tree.get_all_descendants() if n.relation == "root"]
        
        if len(root) == 1:
            aux = [n for n in root[0].children if n.relation == "aux" and n.lemm in ["must", "should", "may", "might", "can", "could", "need", "ought", "shall"]]
            if len(aux) == 1:
                annotations.append(
                    IGTag(words=[(aux[0].id, aux[0].value)], tag_name=IGElement.DEONTIC, tag_id = None)
                )
        return component_id

class AimExtension(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag], component_id):
        aim_node = find_node_with_tag(annotations, tree, IGElement.AIM)

        if aim_node is None:
            return

        for c in aim_node.children:
            if (c.relation in ["aux:pass", "cop"]) or (c.relation == "aux" and c.lemm in ["be", "have", "do"]) or (c.relation == "advmod" and c.lemm == "not"):
                annotations.append(
                    IGTag(words=[(c.id, c.value)], tag_name=IGElement.AIM, tag_id = None)
                )
        return component_id


class Attribute(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag], component_id):
        found_nsubj = False

        for c in tree.children:
            words = {'ATTRIBUTE': [], 'ATTRIBUTE_PROPERTY': []}
            if c.relation in ["nsubj", "nsubj:pass"]:
                for cc in c.get_all_descendants():
                    tag_name = None
                    if cc == c or (cc.relation == "det" and cc.parent == c.id):
                        words['ATTRIBUTE'].append((cc.id, cc.value))
                    else:
                        words['ATTRIBUTE_PROPERTY'].append((cc.id, cc.value))

                if words['ATTRIBUTE']:
                    annotations.append(
                        IGTag(
                            words=words['ATTRIBUTE'],
                            tag_name=IGElement.ATTRIBUTE,
                            tag_id = component_id 
                        )
                    )
                if words['ATTRIBUTE_PROPERTY']:
                    annotations.append(
                        IGTag(
                            words=words['ATTRIBUTE_PROPERTY'],
                            tag_name=IGElement.ATTRIBUTE_PROPERTY,
                            tag_id = component_id + 1
                        )
                    )
                component_id += 2            
        return component_id


class Objects(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag], component_id):
        root = [n for n in tree.get_all_descendants() if n.relation == "root"]

        obj_found = False
        for c in tree.children:
            if c.relation == "obj" :
                words = {'OBJECT_DIRECT': [], 'OBJECT_DIRECT_PROPERTY': []}
                for cc in c.get_all_descendants():
                    tag_name = None
                    if cc == c or (cc.relation in ["det", "amod"] and cc.parent == cc.id): 
                        obj_found = True
                        words['OBJECT_DIRECT'].append((cc.id, cc.value)) 
                    else:
                        words['OBJECT_DIRECT_PROPERTY'].append((cc.id, cc.value)) 
                
                if words['OBJECT_DIRECT']:
                    annotations.append(
                        IGTag(
                            words=words['OBJECT_DIRECT'],
                            tag_name=IGElement.OBJECT_DIRECT,
                            tag_id = component_id 
                        )
                    )
                if words['OBJECT_DIRECT_PROPERTY']:
                    annotations.append(
                        IGTag(
                            words=words['OBJECT_DIRECT_PROPERTY'],
                            tag_name=IGElement.OBJECT_DIRECT_PROPERTY,
                            tag_id = component_id + 1
                        )
                    )
                component_id += 2   

            elif c.relation == "xcomp":
                for cc in c.children:
                    if cc.relation == "obj":
                        annotations.append(
                            IGTag(
                                words=[(cc.id, cc.value)],
                                tag_name=IGElement.OBJECT_DIRECT, tag_id = component_id
                            )
                        )
                        annotations.append(
                            IGTag(
                                words=[(ccc.id, ccc.value) for ccc in cc.get_all_descendants() if ccc != cc],
                                tag_name=IGElement.OBJECT_DIRECT_PROPERTY, tag_id = component_id 
                            )
                        )
                    component_id += 1

            elif c.relation == "conj":
                for cc in c.get_all_descendants():
                    if cc.relation != "cc":
                        IGTag(
                        words=[(cc.id, cc.value)],
                        tag_name=IGElement.OBJECT_DIRECT_PROPERTY, tag_id = component_id
                        )
                component_id +=1

            elif c.relation == "ccomp":
                annotations.append(
                    IGTag(
                        words=[(cc.id, cc.value) for cc in c.get_all_descendants()],
                        tag_name=IGElement.OBJECT_DIRECT, tag_id = component_id
                    )
                )
                component_id += 1

            # elif c.relation == "obl":    
            #     for cc in c.get_all_descendants():
            #         tag_name = None
            #         if cc == c and not obj_found:  
            #             tag_name = IGElement.OBJECT_DIRECT
            #         else:
            #             tag_name = IGElement.OBJECT_DIRECT_PROPERTY
            #         if tag_name:
            #             annotations.append(
            #                 IGTag(
            #                     words=[(cc.id, cc.value)],
            #                     tag_name=tag_name,
            #                 )
            #             )
        return component_id


class Context(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag], component_id):

        for c in tree.children:
            if c.relation == "obj" :
                for cc in c.get_all_descendants():
                    if cc.relation == "advcl":
                        annotations.append(
                            IGTag(
                                words=[(ccc.id, ccc.value) for ccc in cc.get_all_descendants()],
                                tag_name=IGElement.CONTEXT,tag_id = component_id
                            )
                        )
                    component_id += 1
                    
            if c.relation == "advcl":
                for cc in c.get_all_descendants():
                    annotations.append(
                        IGTag(
                            words=[(cc.id, cc.value) for cc in c.get_all_descendants()],
                            tag_name=IGElement.CONTEXT, tag_id = component_id                        )
                    )
                    component_id += 1

            elif c.relation == "obl":
                annotations.append(
                    IGTag(
                        words=[(cc.id, cc.value) for cc in c.get_all_descendants()],
                        tag_name=IGElement.CONTEXT, tag_id = component_id 
                    )
                )
                component_id += 1

            elif c.relation == "advmod" and c.lemm != "not":
                annotations.append(
                    IGTag(
                        words=[(cc.id, cc.value) for cc in c.get_all_descendants()],
                        tag_name=IGElement.CONTEXT, tag_id = component_id                     )
                )
                component_id += 1

            elif c.relation == "xcomp":
                for cc in c.children:
                    if cc.relation in ["obl", "advmod"]:   
                        annotations.append(
                            IGTag(
                                words=[(ccc.id, ccc.value) for ccc in cc.get_all_descendants()],
                                tag_name=IGElement.CONTEXT, tag_id = component_id
                            )
                        )
                    else:
                       annotations.append(
                            IGTag(
                                words=[(ccc.id, ccc.value) for ccc in cc.get_all_descendants()],
                                tag_name=IGElement.CONTEXT, tag_id = component_id
                            )
                        ) 
                    component_id += 1


            elif c.relation == "conj":
                for cc in c.children: 
                    if cc.relation == "xcomp":
                        for ccc in cc.children:
                            if ccc.relation in ["obl", "advmod"]:   
                                annotations.append(
                                    IGTag(
                                        words=[(cccc.id, cccc.value) for cccc in ccc.get_all_descendants()],
                                        tag_name=IGElement.CONTEXT, tag_id = component_id
                                    )
                                )
                    component_id += 1
        return component_id

class Separator(Rule):
    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag], component_id):

        if find_word_igelement(annotations, tree.id) != IGElement.AIM:
            return

        for c in tree.children:
            if c.relation == "punct":
                annotations.append(
                    IGTag(words=[(c.id, c.value)], tag_name=IGElement.SEPARATOR, tag_id = None)
                )

        return component_id
