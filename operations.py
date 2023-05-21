from GameNetworkProtocol import connection as conn
from GameNetworkProtocol.operations import Operation

class Pos(Operation):
    length = 0 #FIXME

    def handle(self, parent_conn:conn.Connection):
        pass

    #use init to make new instance with parameters
    def __init__(self):
        pass

    def encode(self):
        pass

    @classmethod
    def from_data(cls, data:bytes):
        pass


class Attack(Operation):
    length = 0 #FIXME

    def handle(self, parent_conn:conn.Connection):
        pass

    def __init__(self):
        pass

    def encode(self):
        pass

    @classmethod
    def from_data(cls, data:bytes):
        pass

class Hit(Operation):
    length = 0 #FIXME

    def handle(self, parent_conn:conn.Connection):
        pass

    def __init__(self):
        pass

    def encode(self):
        pass

    @classmethod
    def from_data(cls, data:bytes):
        pass

class BlockStart(Operation):
    length = 1

    def handle(self, parent_conn: conn.Connection):
        pass

class BlockStop(Operation):
    length = 1

    def handle(self, parent_conn: conn.Connection):
        pass

class Jump(Operation):
    length = 0 #FIXME

    def handle(self, parent_conn:conn.Connection):
        pass

    def __init__(self):
        pass

    def encode(self):
        pass

    @classmethod
    def from_data(cls, data:bytes):
        pass

class DodgeStart(Operation):
    length = 1

    def handle(self, parent_conn: conn.Connection):
        pass

class DodgeStop(Operation):
    length = 1

    def handle(self, parent_conn: conn.Connection):
        pass

class Death(Operation):
    length = 1

    def handle(self, parent_conn: conn.Connection):
        pass