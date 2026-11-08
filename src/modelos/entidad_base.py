from abc import ABC, abstractmethod

class Entidad(ABC):
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self):
        pass
    