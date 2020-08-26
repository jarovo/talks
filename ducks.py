from typing import Protocol
from abc import abstractmethod, ABCMeta


class Quack:
    def __init__(self, sound_level: int):
        self.sound_level = sound_level


class LureQuack(Quack):
    pass


# ABCMeta needed for PyType https://github.com/google/pytype/issues/214
class CanQuack(Protocol, metaclass=ABCMeta):
    sound_level: int

    @abstractmethod
    def talk(self) -> Quack: ...


class Duck(CanQuack):
    sound_level = 1

    def talk(self) -> Quack:
        return Quack(self.sound_level)


class Lure:
    sound_level = 100

    def talk(self) -> LureQuack:
        return LureQuack(self.sound_level)


class BrokenDuck:
    sound_level = 0

    def talk(self) -> object:
        return object()


def use_as_duck(duck: CanQuack):
    return duck.talk()


use_as_duck(Duck())
use_as_duck(Lure())
use_as_duck(BrokenDuck())