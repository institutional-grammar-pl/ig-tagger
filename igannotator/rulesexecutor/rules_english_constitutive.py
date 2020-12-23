from igannotator.rulesexecutor.rules import *

class ConstitutiveRules(Rule):

    def apply(self, tree: LexcialTreeNode, annotations: List[IGTag], component_id):

        root = [n for n in tree.get_all_descendants() if n.relation == "root"]
        if len(root) == 1:
            print('root', root[0])
            if root[0].tag == 'VERB':
                print('root is verb')
                annotations.append(
                    IGTag(words=[(root[0].id, root[0].value)], tag_name=IGElement.CONSTITUTED_FUNCTION, tag_id = None)
                )

                aux_pass = [n for n in root[0].children if n.relation == "aux:pass"]
                if len(aux_pass) == 1:
                    annotations.append(
                        IGTag(words=[(aux_pass[0].id, aux_pass[0].value)], tag_name=IGElement.CONSTITUTED_FUNCTION, tag_id = None)
                    )

                nsubj = [w for w in root[0].children if w.relation in ["nsubj", "nsubj:pass"] ]
                print('nsubj', nsubj)
                for w in nsubj:
                    annotations.append(
                        IGTag(words=[(ww.id, ww.value) for ww in w.get_all_descendants()], tag_name=IGElement.CONSTITUTED_ENTITY, tag_id = None)
                    )  

                obl = [w for w in root[0].children if w.relation in ["obl"]]
                print('obl', obl)
                for w in obl:
                    annotations.append(
                        IGTag(words=[(ww.id, ww.value) for ww in w.get_all_descendants()], tag_name=IGElement.CONSTITUTING_PROPERTIES, tag_id = component_id)
                    )  
                    component_id += 1                 

            elif root[0].tag == 'noun':
                csubj = [n for n in root[0].children if n.relation == "csubj"]
                if len(csubj) == 1:
                    annotations.append(
                        IGTag(words=[(csubj[0].id, csubj[0].value)], tag_name=IGElement.CONSTITUTED_FUNCTION, tag_id = None)
                    )
                else:
                    cop = [n for n in root[0].children if n.relation == "cop"]
                    if len(cop) == 1:
                        annotations.append(
                            IGTag(words=[(cop[0].id, cop[0].value)], tag_name=IGElement.CONSTITUTED_FUNCTION, tag_id = None)
                        ) 
                det = [n for n in root[0].children if n.relation ==  "det"]
                acl = [n for n in root[0].children if n.relation == "acl"]
                nmod_npmod = [n for n in root[0].children if n.relation == "nmod:npmod "]

                for w in det, acl, nmod_npmod:
                    annotations.append(
                       IGTag(words=[(w[0].id, w[0].value)], tag_name=IGElement.CONSTITUTED_ENTITY, tag_id = component_id)
                    )
                    component_id += 1 
                    annotations.append(
                       IGTag(words=[(ww[0].id, ww[0].value) for ww in w.get_all_descendants() 
                        if ww!= w and ww.relation not in ['mark', 'det']], tag_name=IGElement.CONSTITUTING_PROPERTIES, tag_id = component_id)
                    ) 
                    component_id += 1
                
                for w in acl:
                    mark = [ww for ww in n.children if ww!= w and ww.relation == 'mark']
                    annotations.append(
                       IGTag(words=[(w[0].id, w[0].value) for w in mark], tag_name=IGElement.CONSTITUTED_ENTITY, tag_id = component_id)
                    )
                    component_id += 1

                nsubj = [w for w in root[0].children if w.relation in ["nsubj", "nsubj:pass"] ]
                for w in nsubj:
                    annotations.append(
                        IGTag(words=[(ww[0].id, ww[0].value) for ww in w.get_all_descendants()], tag_name=IGElement.CONSTITUTING_PROPERTIES, tag_id = component_id)
                    )                
                    component_id += 1

            elif root[0].tag == 'propn':
                cop = [n for n in root[0].children if n.relation == "cop"]
                if len(cop) == 1:
                    annotations.append(
                        IGTag(words=[(cop[0].id, cop[0].value)], tag_name=IGElement.CONSTITUTED_FUNCTION, tag_id = None)
                    )  

            aux = [n for n in root[0].children if n.relation == "aux" and n.lemm in ["must", "should", "may", "might", "can", "could", "need", "ought", "shall"]]
            if len(aux) == 1:
                annotations.append(
                    IGTag(words=[(aux[0].id, aux[0].value)], tag_name=IGElement.CONSTITUTED_DEONTIC, tag_id = None)
                )

        for c in tree.children:
            if c.relation == "punct":
                annotations.append(
                    IGTag(words=[(c.id, c.value)], tag_name=IGElement.CONSTITUTED_SEPARATOR, tag_id = None)
                )
        return component_id