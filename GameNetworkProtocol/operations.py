#TODO make abstract?
from abc import ABC, abstractmethod


class Operation(ABC):
    time:int = 0 #TODO initialize or no?

    @property
    @abstractmethod
    def num(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def encode(self):
        raise NotImplementedError

op_list:list[Operation] = list[Operation](

)

class Pos(Operation):
    num = 0

    def encode(self):
        pass