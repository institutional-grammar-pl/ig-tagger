import re

import spacy

spacy_model_name = 'en_core_web_sm'
if not spacy.util.is_package(spacy_model_name):
    spacy.cli.download(spacy_model_name)
nlp = spacy.load(spacy_model_name)


def filter_sentence(sentence):
    def sentence_length(s, min_len=8):
        if len(s) < min_len:
            return False
        else:
            return True
    filters = [sentence_length]
    return all([filter_(sentence) for filter_ in filters])


def gen_atomic_statements(sentence):
    """
    obsługuje sytuację (1) ..., (2) ...
    :param sentence:
    :return:
    """
    rex = r"\([abcdefghi123456789]\)([A-z \n,–:;-]+(\(?(?=[A-z]{2,})[A-z]+\)?[A-z \n,-–;]+)+)"
    splits = re.split(rex, sentence)
    main_sentence = splits[0] if splits is not None else None
    subsentences = re.findall(rex, sentence)

    atomic_statements = []
    if main_sentence and subsentences:
        clean_main_sentence = re.sub(r'\([abcdefgh123456789]\)|\n', ' ', main_sentence).strip()
        for subsentence in subsentences:
            clean_subsentence = re.sub(r'\([abcdefgh123456789]\)|\n', ' ', subsentence[0]).strip()
            atomic_statements.append(clean_main_sentence + ' ' + clean_subsentence + '.')
        return atomic_statements
    else:
        return sentence

