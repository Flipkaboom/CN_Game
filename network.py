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
    s.connect(('8.8.8.8', 80))
    address = (s.getsockname()[0], port)

    initialized = True

def join(ip:str, port:int):
    global initialized
    if not initialized:
        raise Exception('Tried to join group with un-initialized network')

    Gnp.join_group((ip, port))

def active_conns() -> list[Gnp.conn.Connection]:
    res = list()
    for c in Gnp.gl.connections.values():
        if c.knows_peer and not c.closed:
            res.append(c)
    return res

