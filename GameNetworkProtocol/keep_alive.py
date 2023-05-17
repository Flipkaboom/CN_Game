import time

from GameNetworkProtocol import globals as gl, connection as conn

def keep_alive_thread():
    while not gl.kill_threads_flag:
        time.sleep(conn.CONN_TIMEOUT/4)
        for c in gl.connections.values():
            c.send_new_ack()