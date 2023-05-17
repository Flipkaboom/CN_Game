import socket
from GameNetworkProtocol import globals as gl
from GameNetworkProtocol import connection as conn

def global_recv_thread():
    gl.sock.settimeout(1)
    while not gl.kill_threads_flag:
        try:
            data, conn_info = gl.sock.recvfrom(gl.MAX_PACKET_SIZE)
        except socket.timeout:
            continue

        if not (conn_info in gl.connections):
            print('Received connection from: ', conn_info)
            #FIXME mutex with connect_to (and others that add to connection list)
            gl.connections[conn_info] = conn.Connection(conn_info)

        gl.connections[conn_info].recv_packet(data)