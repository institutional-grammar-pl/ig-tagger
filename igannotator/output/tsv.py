from collections import defaultdict
from typing import List, Tuple, Dict

from igannotator.annotator.lexical_tree import LexcialTreeNode
from igannotator.rulesexecutor.rules import IGTag, find_word_tag


def get_sentence_and_tags(
    tree: LexcialTreeNode, tags: List[IGTag]
) -> Tuple[str, List[Tuple[str, int, int, str]]]:
    sentence = ""
    id_to_position = dict()
    for x in tree.get_all_descendants():
        word = str(x.value)
        if x.tag != "PUNCT":
            id_to_position[x.id] = len(sentence) 
            sentence += word + " "
        else:
            id_to_position[x.id] = len(sentence)
            sentence += word
    tag_names = {
        "IGElement.AIM": "(I) Aim",
        "IGElement.ATTRIBUTE": "(A) Attribute",
        "IGElement.ATTRIBUTE_PROPERTY": "(A, prop) Attribute_Property",
        "IGElement.OBJECT": "Object",
        "IGElement.ACTOR": "(A, prop) Attribute_Property",
        "IGElement.OBJECT_DIRECT": "(Bdir) Object_Direct",
        "IGElement.OBJECT_DIRECT_PROPERTY": "(Bdir, prop) Object_Direct_Property",
        "IGElement.EXEC_CONSTRAINT": "(Cex) Execution Constraint",
        "IGElement.SEPARATOR": "(S) Separator",
        "IGElement.DEONTIC": "(D) Deontic",
        "IGElement.ACTIVATION_CONDITION": "(Cac) Activation Condition",
        "IGElement.CONTEXT": "(C) Context",
        "IGElement.CONSTITUTED_ENTITY": "Entity",
        "IGElement.CONSTITUTED_FUNCTION": "Function",
        "IGElement.CONSTITUTING_PROPERTIES": "Properties",
        "IGElement.CONSTITUTED_DEONTIC": "Deontic",
        "IGElement.CONSTITUTED_CONTEXT": "Context",
        "IGElement.CONSTITUTED_SEPARATOR": "Separator"
    }

    tags_tuples = list()

    for x in tree.get_all_descendants():

        if type(x.value) == float:
            x.value = str(int(x.value))
        tag = find_word_tag(tags, x.id)
        start = id_to_position[x.id]
        stop = id_to_position[x.id] + len(str(x)) 
        if tag is None:
            tags_tuples.append(
             (str(x), x.id, start, stop, '-', '')
             )
        else:
            tags_tuples.append(
             (str(x), x.id, start, stop, tag_names[str(tag.tag_name)], tag.tag_id)
            )
    return (sentence, tags_tuples)


def write_tsv_representation(
    output_file, trees_with_tags: List[Tuple[LexcialTreeNode, List[IGTag]]]
):  
    sentences_with_tags = [
        get_sentence_and_tags(tree, tags) for tree, tags in trees_with_tags
    ]

    with open(output_file, "w", encoding="utf-8") as output:

        output.write('#FORMAT=WebAnno TSV 3.2\n')
        output.write('#T_SP=webanno.custom.IGCoreRegulativeSyntax|Additionallabels|Animacy|Circumstance|Component|Impliesnegation|Inferredcomponentvalue|InstitutionalStatement|PhysicalEntity|RegulativeFunction\n')
        output.write('\n')
        output.write('\n')

        text = "\n\n".join([sentence for sentence, _ in sentences_with_tags])
    
        offset = 0
        for index, (sentence, tags) in enumerate(sentences_with_tags):
        
            output.write('#Text='+sentence+'\n')
            for index_tag, (tag_text, tag_id, start, stop, tag_name, component_id) in enumerate(tags):
                if component_id in [None, '']:
                    component_id = ''
                else:
                    component_id = '[' + str(component_id) + ']'
                string = str(index + 1) + "-" + str(tag_id) + "\t"
                span = str(offset+start)+"-"+str(offset + stop)
                string = string + span + "\t"
                string = string + tag_text + "\t"
                string += "*" + component_id + "\t*" + component_id + "\t*" + component_id + "\t"
                if tag_name == 'None':
                    string += "_\t"
                else:
                    string = string + tag_name + str(component_id) + "\t"
                string += "false" + component_id + "\t*" + component_id + "\tfalse" + component_id + "\tfalse" + component_id + "\t*" + component_id + "\t"
                output.write(string + '\n')
            offset += len(sentence) + 2
            if not index == len(sentences_with_tags) - 1: output.write('\n')