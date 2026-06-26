from abc import ABC, abstractmethod

class OCREngine(ABC):

    @abstractmethod
    def read(self, page):
        pass