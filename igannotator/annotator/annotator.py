from abc import ABC, abstractmethod
import pathlib

class BaseAnnotator(ABC):
    def __init__(self):
        self.resources_dir = str(pathlib.Path('~/.cache/ig/models/').expanduser().absolute())

    @abstractmethod
    def annotate(self, text: str):
        raise NotImplementedError()