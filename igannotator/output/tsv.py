from typing import List, Tuple

import numpy

from igannotator.annotator.lexical_tree import LexicalTreeNode
from igannotator.rulesexecutor.rules import IGTag, find_word_tag


def get_sentence_and_tags(

        tree: LexicalTreeNode, tags: List[IGTag], layers: []
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
        "IGElement.OBJECT": "(B) Object",
        "IGElement.OBJECT_PROPERTY": "(B, prop) Object_Property",
        "IGElement.DEONTIC": "(D) Deontic",
        "IGElement.CONTEXT": "(C) Context",

        "IGElement.CONSTITUTED_ENTITY": "(E) Constituted Entity",
        "IGElement.CONSTITUTED_ENTITY_PROPERTY": "(E, prop) Constituted Entity Property",
        "IGElement.CONSTITUTIVE_FUNCTION": "(F) Constitutive Function",
        "IGElement.CONSTITUTING_PROPERTIES": "(P) Constituting Properties",
        "IGElement.CONSTITUTING_PROPERTIES_PROPERTY": "(P) Constituting Properties Property",
        "IGElement.MODAL": "(M) Modal"
    }

    results = {}

    for word_id, x in enumerate(tree.get_all_descendants()):

        if type(x.value) == float:
            x.value = str(int(x.value))

        word_tags = find_word_tag(tags, x.id, layers)

        # if len(word_tags[layers[0]]) > 2:
        #     print("exit! word with multiple tags found")
        #     exit(word_tags[layers[0]])
        if len(word_tags[layers[0]]) > 2:
            word_tags[layers[0]] = [word_tags[layers[0]][0]]

        start = id_to_position[x.id]
        stop = id_to_position[x.id] + len(str(x))

        word_data = {'word': str(x), 'word_id': x.id, 'start': start, 'stop': stop,
                     'tags': {'reg': {'depth_1': [], 'depth_2': []}, 'cons': {'depth_1': [], 'depth_2': []}}}

        for layer in layers:
            if word_tags[layer] == []:
                word_data['tags'][layer]['depth_1'].append({'tag_name': '', 'tag_id': ''})
                word_data['tags'][layer]['depth_2'].append({})
            elif len(word_tags[layer]) == 1:
                word_data['tags'][layer]['depth_1'].append(
                    {'tag_name': tag_names[str(word_tags[layer][0].tag_name)], 'tag_id': word_tags[layer][0].tag_id})
                word_data['tags'][layer]['depth_2'].append({})
            else:
                word_data['tags'][layer]['depth_1'].append(
                    {'tag_name': tag_names[str(word_tags[layer][0].tag_name)], 'tag_id': word_tags[layer][0].tag_id})
                word_data['tags'][layer]['depth_2'].append(
                    {'tag_name': tag_names[str(word_tags[layer][1].tag_name)], 'tag_id': word_tags[layer][1].tag_id})
        results[word_id] = word_data

    return results


def write_tsv_representation(
        output_file, trees_with_tags: List[Tuple[LexicalTreeNode, List[IGTag]]], layers: List[str],
        index: List[numpy.int64]
):
    with open(output_file, "w", encoding="utf-8") as output:
        output.write('#FORMAT=WebAnno TSV 3.2\n')
        layers = sorted(layers)
        if 'cons' in layers:
            output.write('#T_SP=webanno.custom.IGCoreConstitutiveSyntax|Component\n')
        if 'reg' in layers:
            output.write('#T_SP=webanno.custom.IGCoreRegulativeSyntax|Component\n')
        output.write('\n')
        output.write('\n')

        offset = 0
        for sent_id, (sentence, tree, tags) in enumerate(trees_with_tags):
            output.write('#Text=' + sentence + '\n')
            results = get_sentence_and_tags(tree, tags, layers)
            for word_data in results.values():
                sent_word = str(sent_id + 1) + "-" + str(word_data['word_id'])
                span = ''.join([str(offset + word_data['start']), "-", str(offset + word_data['stop'])])
                word = word_data['word']
                line = [str(index[sent_id]), sent_word, span, word]
                for layer in layers:
                    word_tags = ''
                    for depth in ['depth_1', 'depth_2']:
                        tag_name, tag_id = None, None

                        if word_data['tags'][layer][depth] == []:
                            word_data['tags'][layer][depth] = [{}]

                        if 'tag_name' in word_data['tags'][layer][depth][0].keys():
                            tag_name = word_data['tags'][layer][depth][0]['tag_name']
                            tag_id = word_data['tags'][layer][depth][0]['tag_id']
                        tag_id = ''.join(['[', str(tag_id), ']']) if tag_id else ''
                        tag_name = tag_name + tag_id if tag_name else ''

                        if depth == 'depth_1':
                            word_tags = tag_name
                        if depth == 'depth_2' and tag_name != '':
                            word_tags = word_tags + '|' + tag_name
                    line.append(word_tags)
                string = '\t'.join(line)
                output.write(string + '\n')
            offset += len(sentence) + 2
            if not sent_id == len(trees_with_tags) - 1:
                output.write('\n')
