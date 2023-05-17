from GameNetworkProtocol import globals as gl
from GameNetworkProtocol import interface as interface
import threading

interface.initialize('Flip')

print('Self:')
print(gl.sock.getsockname())