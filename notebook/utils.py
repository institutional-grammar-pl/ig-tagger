import difflib
import re


MAP_NAMES = {
    'Attributes (Content)': "(A) Attribute", 
    'Attributes property (Content)': "(A, prop) Attribute_Property",
    'Attributes property (Reference to statement)': "(A, prop) Attribute_Property", 
    'Deontic': "(D) Deontic", 
    'Aim': "(I) Aim",
    'Direct Object (Content)': "(B) Object", 
    'Direct Object (Reference to statement)': "(B, prop) Object_Property",
    'Direct Object Property': "(B, prop) Object_Property", 
    'Indirect Object': "(B) Object", 
    'Activation Condition (Content)':   "(C) Context",
    'Execution Constraint (Content)':   "(C) Context",
    'Constituted Entity (Content)': "(E) Constituted Entity", 
    'Constituted Entity Property (Content)':  "(E, prop) Constituted Entity Property",
    'Constituted Entity Property (Reference to statement)':  "(E, prop) Constituted Entity Property", 
    'Modal': "(M) Modal",
    'Function': "(F) Constitutive Function", 
    'Constituted Properties (Content)':  "(P) Constituting Properties",
    'Constituted Properties Property (Content)': "(P) Constituting Properties Property",
    'Activation Condition (Content).1': "(C) Context",
    'Activation Condition (Reference to statement).1': "(C) Context",
    'Execution Constraint (Content).1': "(C) Context",
    'Execution Constraint (Reference to statement).1': "(C) Context"
}



def load_gs(gold_standard):
    gs = []
    for i, x in gold_standard.iterrows():
        temp = {
            'id': i,
            'sentence': x['Statement'],
            'tags':[]
        }

        tag_temp = x[6:]
        tag_temp = tag_temp[~tag_temp.isna()]
        for index, value in tag_temp.iteritems():
            if index in MAP_NAMES:
                for val in re.split(r" |-|\[|\]", str(value)):
                    temp['tags'].append((val, MAP_NAMES[index]))
        gs.append(temp)
    return gs


def find_goldstandard(sentence, gs):
    for elem in gs:
        if sentence == elem['sentence']:
            return elem


def find_tag(word, tags):

    for elem in tags:
        if elem[0] == word:
            return elem[1]
    return ""


def write_gs(title, path_data, gs):
    text = None
    real_tag = None
    with open(path_data.joinpath(f"{title}.tsv"), "r", encoding="utf-8") as f,\
        open(path_data.joinpath(f"{title}_gs.tsv"), "w", encoding="utf-8") as f_output:
        for i, row in enumerate(f):
            if i > 3:
                if row.startswith("#Text="):
                    f_output.write("\n")
                    text = row.split("Text=")[1]
                    real_tag = find_goldstandard(text[:-1], gs)
                    f_output.write(row)
                    f_output.write("\n")
                elif row != "\n":
                    splitted_row = row.split("\t")
                    word = splitted_row[2]
                    tag = find_tag(word, real_tag['tags'])
                    output = splitted_row[-2] + "\t" + splitted_row[-1].split("[")[0].replace("\n", "") + "\t" + tag + "\n"
                    if word.lower() not in [".", "-", "(", ")", "[", "]", ",", "the", "a", "an"]:
                        f_output.write(output)


def load_evaluation_data(file_name, path_data):
    golds = []
    preds = []

    with open(path_data.joinpath(file_name), "r", encoding="utf-8") as f:
        for row in f:
            if not row.startswith("#Text=") and not (row == "\n") and not (row.split("\t")[0] == "\n"):
                splitted_row = row.split("\t")
                golds.append(splitted_row[-1].replace("\n", ""))
                preds.append(splitted_row[-2].replace("\n", ""))
    map_names = {
        "(E, prop) Constituted Entity Property": "(E) Constituted Entity",
        "(P) Constituting Properties Property": "(P) Constituting Properties",
        "(F) Constitutive Function|(C) Context": "(F) Constitutive Function",
        "(A, prop) Attribute_Property": "(A) Attribute",
        "(B, prop) Object_Property": "(B) Object"
    }
    preds = [map_names.get(item, item) for item in preds]
    golds = [map_names.get(item, item) for item in golds]
    return preds, golds
