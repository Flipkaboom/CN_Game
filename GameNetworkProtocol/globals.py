import queue
import socket
import threading

from . import connection as conn

MAX_PACKET_SIZE = 512

sock:socket.socket

player_name = 'UNSET'
conn_id = -1

kill_threads_flag = False
ready_for_init = True

t_recv:threading.Thread
t_alive:threading.Thread

conn_lock:threading.Lock = threading.Lock()
connections:dict[tuple, conn.Connection] = dict[tuple, conn.Connection]()

events:list[tuple[str, object]] = list[tuple[str, object]]()

incoming_drop_chance:int = 0
outgoing_drop_chance:int = 0
