import socket

from GameNetworkProtocol import connection as conn

MAX_PACKET_SIZE = 2048

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 0))

#FIXME init properly
player_name = 'Flip'
conn_id = 1234

connections:dict[tuple, conn.Connection] = dict[tuple, conn.Connection]()