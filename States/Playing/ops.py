from GameNetworkProtocol import connection as conn
from GameNetworkProtocol.operations import Operation
import instance as inst
from States.Playing import playing

class Pos(Operation):
    length = 21

    pos:tuple[int, int]
    speed:tuple[int, int]
    up:bool
    left:bool
    down:bool
    right:bool

    def handle(self, parent_conn:conn.Connection):
        s:playing.Playing = inst.state
        try:
            p = s.players[parent_conn.address]
        except KeyError:
            print('Received data from non-existing player')
            return

        # print('Received pos ', self.pos)

        p.set_pos(self.pos)
        p.speed = self.speed
        p.controls_up = self.up
        p.controls_left = self.left
        p.controls_down = self.down
        p.controls_right = self.right
        p.received_network = True



    #use init to make new instance with parameters
    def __init__(self, pos:tuple[int, int], speed:tuple[int, int], up:bool, left:bool, down:bool, right:bool):
        self.pos = pos
        self.speed = speed
        self.up = up
        self.left = left
        self.down = down
        self.right = right

    def encode(self):
        return self._encode_values((self.pos[0], self.pos[1], self.speed[0], self.speed[1]),
                                   (self.up, self.left, self.down, self.right))

    @classmethod
    def from_data(cls, data:bytes):
        pos_x, pos_y, speed_x, speed_y, up, left, down, right = Operation._decode_values(data, num_ints=4, num_chars=4)
        return cls((pos_x, pos_y), (speed_x, speed_y), up, left, down, right)


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