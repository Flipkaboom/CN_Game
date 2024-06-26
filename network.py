import socket

import GameNetworkProtocol as Gnp
from GameNetworkProtocol.interface import get_events, queue_op, send_all, handle_all
import instance as inst

address:tuple
initialized:bool = False

def init():
    global address, initialized
    _, port = Gnp.initialize(inst.name)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('8.8.8.8', port))
        address = (s.getsockname()[0], port)
    except Exception:
        address = ('127.0.0.1', port)
    finally:
        s.close()

    initialized = True

def join(ip:str, port:int):
    global initialized
    if not initialized:
        raise Exception('Tried to join group with un-initialized network')

    Gnp.join_group((ip, port))

def active_conns() -> list[Gnp.conn.Connection]:
    res = list()
    with Gnp.conn_lock:
        for c in Gnp.gl.connections.values():
            if c.knows_peer and not c.closed:
                res.append(c)
    return res

def get_incoming_drop_chance() -> int:
    return Gnp.gl.incoming_drop_chance

def get_outgoing_drop_chance() -> int:
    return Gnp.gl.outgoing_drop_chance

def set_incoming_drop_chance(chance:int):
    Gnp.gl.incoming_drop_chance = chance

def set_outgoing_drop_chance(chance:int):
    Gnp.gl.outgoing_drop_chance = chance