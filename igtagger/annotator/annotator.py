from abc import ABC
import pathlib


class BaseAnnotator(ABC):
    def __init__(self):
        self.resources_dir = str(pathlib.Path('~/.cache/ig/models/').expanduser().absolute())
