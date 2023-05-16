import socket
from GameNetworkProtocol import globals as gl
from GameNetworkProtocol import connection as conn

def global_recv_thread():
    while True:
        data, conn_info = gl.sock.recvfrom(gl.MAX_PACKET_SIZE)

        if not (conn_info in gl.connections):
            print('Received connection from:')
            print(conn_info)
            #FIXME mutex with connect_to (and other that add to connection list)
            gl.connections[conn_info] = conn.Connection(conn_info)

        #FIXME connections should be able to timeout individually -> make incoming packet queue then timeout on queue
        #       get in thread for every connection???
        gl.connections[conn_info].handle_incoming(data)