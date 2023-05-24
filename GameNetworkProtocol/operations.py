from abc import ABC, abstractmethod

from . import connection as conn
from . import globals as gl

op_num_counter = 0

class Operation(ABC):
    priority_op:bool = False

    def __init_subclass__(cls, **kwargs):
        global op_num_counter
        cls.num = op_num_counter
        op_num_counter += 1

    length:int

    def encode(self):
        return self.num.to_bytes(1, 'big')

    @classmethod
    def from_data(cls, data:bytes):
        return cls()

    def _encode_values(self, ints:tuple = (), chars:tuple = ()) -> bytes:
        res = bytes()
        res += self.num.to_bytes(1, 'big', signed=True)
        for val in ints:
            res += val.to_bytes(4, 'big', signed=True)
        for val in chars:
            res += val.to_bytes(1, 'big')
        return res

    @staticmethod
    def _decode_values(data:bytes, num_ints:int = 0, num_chars:int = 0) -> list:
        res = list()
        i = 1
        for _ in range(0, num_ints * 4, 4):
            res.append(int.from_bytes(data[i:i + 4], 'big', signed=True))
            i += 4
        for _ in range(0, num_chars):
            res.append(data[i])
            i += 1
        return res


    @abstractmethod
    def handle(self, parent_conn:conn.Connection):
        raise NotImplementedError

    @staticmethod
    def from_num(num:int, data:bytes = bytes()):
        cls = Operation.__subclasses__()[num]
        return cls.from_data(data)


class PlayerInfo(Operation):
    priority_op = True

    def handle(self, parent_conn:conn.Connection):
        #If info was peer's own info, take their address from parent Connection
        if self.ip == '0.0.0.0':
            conn_info = parent_conn.address
        elif self.ip == '127.0.0.1':
            conn_info = (parent_conn.address[0], self.port)
        else:
            conn_info = (self.ip, self.port)

        #If we have seen peer before this is a response so fill in info in connection
        try:
            with gl.conn_lock:
                gl.connections[conn_info].address = conn_info
                gl.connections[conn_info].conn_id = self.conn_id
                gl.connections[conn_info].player_name = self.name
                #If we don't know peer, this is response to connection. Respond with all known players' info
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
                    gl.events.append(('CONNECT', conn_info))
                    gl.connections[conn_info].send_new_outgoing()
        #Else this is a peer sending us info about a player we don't know anything about -> send conn request
        except KeyError:
            conn.connect_to_known(conn_info, self.conn_id, self.name)

    @classmethod
    def my_info(cls):
        return cls('0.0.0.0', gl.sock.getsockname()[1], gl.conn_id, gl.player_name)

    def __init__(self, ip:str, port:int, conn_id:int, name:str):
        self.ip = ip
        self.port = port
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

class Test(Operation):
    length = 5

    def __init__(self, debug_num:int):
        self.debug_num = debug_num

    def encode(self) -> bytes:
        return self._encode_values(ints=(self.debug_num,))

    @classmethod
    def from_data(cls, data:bytes):
        debug_num, = cls._decode_values(data, num_ints=1)
        return cls(debug_num)

    def handle(self, parent_conn: conn.Connection):
        print('Test: ' + str(self.debug_num))