from abc import ABC, abstractmethod


class AccessoriesAbstract(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def add(self, index: int, name: str):
        pass


class CarAbstract(ABC):
    def __init__(self, acc: AccessoriesAbstract):
        self.acc = acc
        super().__init__()

    @abstractmethod
    def run(self):
        pass

class Accessories(AccessoriesAbstract):
    def add(self, index, name):
        pass
class Car(  CarAbstract):
    def run(self):
        pass