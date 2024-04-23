from abc import ABC, abstractmethod

class Processor(ABC):
    @abstractmethod
    def run(self):
        pass