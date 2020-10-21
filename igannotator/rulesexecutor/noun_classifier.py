import requests
import json

from ...igannotator.rulesexecutor.ig_element import IGElement

API_URL = "http://plwordnet.pwr.wroc.pl/wordnet/api/lexemes/"
API_URL_2 = "http://plwordnet.pwr.wroc.pl/wordnet/api/senses/"

ACTOR_DOMAINS = 15


def nounClassifier(word):
    """Classifies noun as actor o object

    Parameters
    ----------
    word : str
        Lematized noun to be classified (case-insensitive).
    """

    word = word.lower()
    response_raw = requests.get(
        API_URL + word
    )
    response = json.loads(response_raw.content)
    response = [
        item for item in response if item["lemma"].lower() == word
    ]
    if len(response) == 0:
        return None
    sense_id = response[0]["sense_id"]
    
    response_raw_2 = requests.get(
        API_URL_2 + sense_id
    )
    response_2 = json.loads(response_raw_2.content)
    domain_id = response_2["domain_id"]
    
    if int(domain_id) == ACTOR_DOMAINS:
        return IGElement.ATTRIBUTE
    else:
        return IGElement.OBJECT

