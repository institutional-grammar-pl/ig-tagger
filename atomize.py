import re

import spacy

# import en_core_web_sm
# nlp = en_core_web_sm.load()
nlp = spacy.load("en_core_web_sm")


def filter_sentence(sentence):
    def sentence_length(s, min_len=8):
        if len(s) < min_len:
            return False
        else:
            return True
    filters = [sentence_length]
    return all([filter_(sentence) for filter_ in filters])


def get_sentences(txt, sentence_split_type='spacy', bare=False, print_=False):
    # remove new lines
    txt = re.sub('\n|:|"|;', ' ', txt)
    if sentence_split_type == 'spacy':  # split text into sentences by spacy
        doc = nlp(txt)
        sents = doc.sents
    elif sentence_split_type == 'regex':  # split text into sentences using regular expressions
        sents = re.split(r"([A-Z][^\.!?]*[\.!?])", txt)
    else:
        raise ValueError()

    result = []
    for ind, s in enumerate(sents):
        if filter_sentence(s):
            curr_sentence = str(s) if bare else gen_atomic_statements(str(s))
            if print_:
                print(f"zdanie nr. {ind} ----------\n{curr_sentence}\n-----------------------")
            result.append('\n\n'.join(curr_sentence) if type(curr_sentence) is list else curr_sentence)

    return result


def gen_atomic_statements(sentence):
    """
    obsługuje sytuację (1) ..., (2) ...
    :param sentence:
    :return:
    """
    rex = r"\([abcdefgh123456789]\)([A-z \n,-]+(\(?(?=[A-z]{2,})[A-z]+\)?[A-z \n,-]+)+)"
    splits = re.split(rex, sentence)
    main_sentence = splits[0] if splits is not None else None
    subsentences = re.findall(rex, sentence)

    atomic_statements = []
    if main_sentence and subsentences:
        clean_main_sentence = re.sub(r'\([abcdefgh123456789]\)|\n', ' ', main_sentence).strip()
        for subsentence in subsentences:
            clean_subsentence = re.sub(r'\([abcdefgh123456789]\)|\n', ' ', subsentence[0]).strip()
            atomic_statements.append(clean_main_sentence + ' ' + clean_subsentence)
        return atomic_statements
    else:
        return sentence


def atomize(input_path, output_path):
    with open(input_path, 'r') as input_:
        text = input_.read()
    sents = get_sentences(text)

    with open(output_path, 'w+') as output:
        output.write('\n\n'.join(sents))
