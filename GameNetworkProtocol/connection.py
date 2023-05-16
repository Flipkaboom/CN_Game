import queue
from collections import deque

from GameNetworkProtocol import globals as gl
from GameNetworkProtocol import helpers as hlp
#operations import at bottom of file

import threading

PORT = 42069
SEQ_INFO_LEN = 5

class Connection:
    #TODO initialize
    player_name:str
    conn_id:int

    #TODO initialize
    address:(str, int)

    knows_peer:bool = False

    seq_num:int = 0
    ack_num:int = 0

    # op_send_list:deque[ops.Operation]
    # op_recv_list:queue.Queue[ops.Operation]

    send_list_lock:threading.Lock


    def __init__(self, address:tuple):
        self.address = hlp.sanitize_address(address)
        self.op_send_list = deque[ops.Operation]()
        self.op_recv_list = queue.Queue[ops.Operation]()
        self.net_op_recv_list = queue.Queue[ops.Operation]()
        self.send_list_lock = threading.Lock()

    def encode_ops(self) -> bytes:
        res = bytes()
        for op in self.op_send_list:
            if len(res) + op.length >= gl.MAX_PACKET_SIZE - SEQ_INFO_LEN:
                break
            res += op.encode()
        return res

    def decode_ops(self, data:bytes, seq_num:int):
        i = 0
        seq_num_counter = seq_num
        while i < len(data):
            num = data[i]
            op = ops.Operation.from_num(num, data[i:])

            if seq_num_counter >= self.ack_num:
                if op.network_op:
                    self.net_op_recv_list.put(op)
                else:
                    self.op_recv_list.put(op)

            i += op.length
            seq_num_counter += 1
        self.ack_num = seq_num_counter

    def encode_seq_num(self) -> bytes:
        res = bytes()
        res += self.seq_num.to_bytes(4, 'big')
        res += (0).to_bytes(1, 'big')
        return res

    @staticmethod
    def decode_sync_info(data:bytes) -> (int, bool):
        return int.from_bytes(data[0:4], 'big'), data[4]

    def handle_incoming_ack(self, ack_num:int):
        if ack_num <= self.seq_num:
            return

        with self.send_list_lock:
            ack_op_count = ack_num - self.seq_num
            #FIXME is this actually better than using a list (instead of deque) and copying using [ack_op_count:]
            for i in range(0, ack_op_count):
                self.op_send_list.popleft()

            self.seq_num = ack_num

    def handle_incoming(self, data:bytes):
        seq_num, is_ack = self.decode_sync_info(data)

        if is_ack:
            self.handle_incoming_ack(seq_num)
        else:
            self.decode_ops(data[SEQ_INFO_LEN:], seq_num)
            while not self.net_op_recv_list.empty():
                #FIXME block receiver thread on receiving something that doesn't contain a PlayerInfo op
                #           Can this ever actually happen??
                op = self.net_op_recv_list.get()
                op.handle(self)
            self.send_new_ack()

    def new_outgoing(self) -> bytes:
        with self.send_list_lock:
            ret = self.encode_seq_num() + self.encode_ops()
        return ret

    def new_outgoing_ack(self) -> bytes:
        res = bytes()
        res += self.ack_num.to_bytes(4, 'big')
        res += (1).to_bytes(1, 'big')
        return res

    def add_op(self, op):
        with self.send_list_lock:
            self.op_send_list.append(op)

    def send_new_outgoing(self):
        gl.sock.sendto(self.new_outgoing(), self.address)

    def send_new_ack(self):
        gl.sock.sendto(self.new_outgoing_ack(), self.address)

    #incoming data      safe
    #incoming ack       affects sender list and seq_num
    #outgoing data      uses sender_list and seq_num
    #outgoing ack       safe

def connect_to(address:tuple, conn_id:int, player_name:str) -> Connection:
    address = hlp.sanitize_address(address)
    if address in gl.connections:
        raise Exception("Address already in connections list")

    print('Connecting to:')
    print( address)

    self = Connection(address)
    #FIXME mutex on this list???
    gl.connections[address] = self
    self.conn_id = conn_id
    self.player_name = player_name
    #FIXME ?
    self.knows_peer = True
    self.add_op(ops.PlayerInfo.my_info())
    self.send_new_outgoing()
    return self

from GameNetworkProtocol import operations as ops
