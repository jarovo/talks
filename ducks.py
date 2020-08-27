from typing import Protocol, overload, Union, Optional
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


def use_qacking_thing(duck: CanQuack):
    return duck.talk()


def deref_none(duck: Optional[Duck]):
    if duck is None:
        return Quack(1)
    duck.talk()


deref_none(None)

use_qacking_thing(Duck())
use_qacking_thing(Lure())
#use_qacking_thing(BrokenDuck())

