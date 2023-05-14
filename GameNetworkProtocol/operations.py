from abc import ABC, abstractmethod

op_num_counter = 0

class Operation(ABC):
    time:int = 0 #TODO initialize or no?

    def __init_subclass__(cls, **kwargs):
        global op_num_counter
        cls.num = op_num_counter
        op_num_counter += 1

    @property
    @abstractmethod
    def length(self) -> int:
        raise NotImplementedError

    def encode(self) -> bytes:
        return self.num.to_bytes(self.length, 'big')

    @classmethod
    def from_data(cls, data:bytes):
        return cls()

    @staticmethod
    def from_num(num:int, data:bytes = bytes()):
        cls = Operation.__subclasses__()[num]
        return cls.from_data(data)


class Pos(Operation):
    #use init to make new instance with parameters
    def __init__(self):
        pass

    def encode(self):
        pass

    @classmethod
    def from_data(cls, data:bytes):
        pass


class Attack(Operation):
    def __init__(self):
        pass

    def encode(self):
        pass

    @classmethod
    def from_data(cls, data:bytes):
        pass

class Hit(Operation):
    def __init__(self):
        pass

    def encode(self):
        pass

    @classmethod
    def from_data(cls, data:bytes):
        pass

class BlockStart(Operation):
    length = 1

class BlockStop(Operation):
    length = 1

class Jump(Operation):
    def __init__(self):
        pass

    def encode(self):
        pass

    @classmethod
    def from_data(cls, data:bytes):
        pass

class DodgeStart(Operation):
    length = 1

class DodgeStop(Operation):
    length = 1

class Death(Operation):
    length = 1

class MatchReady(Operation):
    length = 1

class MatchUnready(Operation):
    length = 1

class ConnRequest(Operation):
    def __init__(self):
        pass

    def encode(self):
        pass

    @classmethod
    def from_data(cls, data:bytes):
        pass

class OtherPlayer(Operation):
    def __init__(self):
        pass

    def encode(self):
        pass

    @classmethod
    def from_data(cls, data:bytes):
        pass