from abc import ABC, abstractmethod

class BaseReport(ABC):
    @abstractmethod
    def generate(self, lines):
        pass
