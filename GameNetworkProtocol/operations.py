from abc import ABC, abstractmethod

from GameNetworkProtocol import globals as gl
from GameNetworkProtocol import connection as conn

op_num_counter = 0

class Operation(ABC):
    #FIXME still needed?
    time:int = 0 #TODO initialize or no?

    network_op:bool = False

    def __init_subclass__(cls, **kwargs):
        global op_num_counter
        cls.num = op_num_counter
        op_num_counter += 1

    length:int

    def encode(self) -> bytes:
        return self.num.to_bytes(self.length, 'big')

    @classmethod
    def from_data(cls, data:bytes):
        return cls()

    @abstractmethod
    def handle(self, parent_conn:conn.Connection):
        raise NotImplementedError

    # @staticmethod
    # def length_from_num(num:int):
    #     cls = Operation.__subclasses__()[num]
    #     return cls.length

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

class PlayerInfo(Operation):
    network_op = True

    def handle(self, parent_conn:conn.Connection):
        #If info was peer's own info, take their address from parent Connection
        if self.ip == '0.0.0.0':
            conn_info = parent_conn.address
        else:
            conn_info = (self.ip, self.port)

        #If we have seen peer before this is a response so fill in info in connection
        if conn_info in gl.connections:
            gl.connections[conn_info].address = conn_info
            gl.connections[conn_info].conn_id = self.conn_id
            gl.connections[conn_info].player_name = self.name
            #If we don't know peer, this is response to connection. Respond with all knows players' info
            if not gl.connections[conn_info].knows_peer:
                #Own player info
                op = PlayerInfo.my_info()
                gl.connections[conn_info].add_op(op)
                #Peer players' info
                for c in gl.connections.values():
                    #Do not send back the client's own info, it doesn't like that because it doesn't know its own ip
                    if c.address != parent_conn.address:
                        op = PlayerInfo(c.address[0], c.address[1], c.conn_id, c.player_name)
                        gl.connections[conn_info].add_op(op)
                gl.connections[conn_info].knows_peer = True
                #FIXME should this send here? Hopefully
                gl.connections[conn_info].send_new_outgoing()
        #Else this is a peer sending us info about a player we don't know anything about -> send conn request
        else:
            gl.connections[conn_info] = conn.connect_to(conn_info, self.conn_id, self.name)

    @classmethod
    def my_info(cls):
        return cls('0.0.0.0', gl.sock.getsockname()[1], gl.conn_id, gl.player_name)

    def __init__(self, ip:str, port:int, conn_id:int, name:str):
        self.ip = ip
        self.port = port
        #FIXME with dynamic port I don't think this does anything, reconnections will already come from a different port
        #           (assuming it doesn't reuse ports (it shouldn't if I don't tell it to))
        self.conn_id = conn_id
        self.name = name
        self.length = 1 + 4 + 4 + 4 + 4 + len(name)

    def encode(self):
        res = bytes()
        res += self.num.to_bytes(1, 'big')
        res += self.length.to_bytes(4, 'big')
        ip_split = self.ip.split('.')
        for num in ip_split:
            res += int(num).to_bytes(1, 'big')
        res += self.port.to_bytes(4, 'big')
        res += self.conn_id.to_bytes(4, 'big')
        res += self.name.encode()
        return res

    @classmethod
    def from_data(cls, data:bytes):
        length = int.from_bytes(data[1:5], 'big')
        ip = ''
        for byte in data[5:9]:
            ip += str(byte)
            ip += '.'
        ip = ip[:-1]
        port = int.from_bytes(data[9:13], 'big')
        conn_id = int.from_bytes(data[13:17], 'big')
        name = data[17:length].decode()
        return cls(ip, port, conn_id, name)