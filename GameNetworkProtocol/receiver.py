import socket
from . import globals as gl
from . import connection as conn
from . import crc

def global_recv_thread():
    gl.sock.settimeout(1)
    while not gl.kill_threads_flag:
        try:
            data, conn_info = gl.sock.recvfrom(gl.MAX_PACKET_SIZE)
        except socket.timeout:
            continue
        except ConnectionResetError:
            continue

        if not crc.valid_crc(data):
            continue

        with gl.conn_lock:
            if not (conn_info in gl.connections):
                print('Received connection from: ', conn_info)
                gl.connections[conn_info] = conn.Connection(conn_info)

        gl.connections[conn_info].recv_packet(data)