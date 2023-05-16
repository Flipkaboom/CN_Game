from GameNetworkProtocol import receiver
from GameNetworkProtocol import globals as gl
from GameNetworkProtocol import connection as conn
from GameNetworkProtocol import operations as ops
import threading
t = threading.Thread(target=receiver.global_recv_thread)
t.daemon = True
t.start()

print('Self:')
print(gl.sock.getsockname())