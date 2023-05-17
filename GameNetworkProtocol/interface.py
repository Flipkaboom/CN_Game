import random
import threading
import socket
import time

from GameNetworkProtocol import connection as conn, globals as gl, receiver as rcv, operations as ops, keep_alive

def initialize(name:str):
    while not gl.ready_for_init:
        time.sleep(1)

    gl.ready_for_init = False
    gl.kill_threads_flag = False
    gl.player_name = name

    gl.conn_id = random.randint(0, 4294967295)

    gl.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    gl.sock.bind(('', 0))

    gl.t_recv = threading.Thread(target=rcv.global_recv_thread)
    gl.t_recv.daemon = True
    gl.t_recv.start()

    gl.t_alive = threading.Thread(target=keep_alive.keep_alive_thread)
    gl.t_alive.daemon = True
    gl.t_alive.start()

    print(f'Listening on port {gl.sock.getsockname()[1]}')

def queue_op(op:ops.Operation):
    for c in gl.connections.values():
        c.add_op(op)

def send_all():
    for c in gl.connections.values():
        c.send_new_outgoing()

def handle_all():
    for c in gl.connections.values():
        c.handle_all()

def connect_to_group(address:tuple):
    if len(gl.connections) > 0:
        raise Exception("Networking already running/connected. Please restart program to retry (this exception probably restarted it for you lol)")
    else:
        conn.connect_to(address, gl.conn_id, gl.player_name)

def close_all():
    if gl.ready_for_init:
        raise Exception("Can't close connection because module was never initialized")

    gl.kill_threads_flag = True

    gl.t_recv.join()
    gl.t_alive.join()

    keys = list[tuple]()
    for key in gl.connections.keys():
        keys.append(key)

    for key in keys:
        gl.connections[key].close()

    gl.player_name = 'UNSET'
    gl.conn_id = -1

    gl.sock.close()

    gl.ready_for_init = True