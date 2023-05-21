import queue
from collections import deque

#This fixes all the circular import issues
class Connection:
    pass

from . import globals as gl
from . import helpers as hlp
from . import operations as ops
from . import crc
#operations import at bottom of file

import threading

SEQ_INFO_LEN = 5
CONN_TIMEOUT = 5
RESEND_TIMEOUT = 0.033333333


# noinspection PyRedeclaration
class Connection:
    player_name:str
    conn_id:int

    address:(str, int)

    knows_peer:bool = False
    closed:bool = False

    seq_num:int = 0
    ack_num:int = 0

    send_until:int = 0

    # op_send_list:deque[ops.Operation]
    # op_recv_list:queue.Queue[ops.Operation]

    send_list_lock:threading.Lock

    resend_timer:threading.Timer


    def __init__(self, address:tuple):
        self.address = hlp.sanitize_address(address)

        self.op_send_list = deque[ops.Operation]()

        #FIXME Apparently deque is much faster than queue so switch that if it runs like shit
        self.op_recv_list = queue.Queue[ops.Operation]()
        self.net_op_recv_list = queue.Queue[ops.Operation]()

        self.data_recv_queue = queue.Queue[bytes]()

        self.data_recv_thread = threading.Thread(target=data_recv_thread, args=(self,))
        self.data_recv_thread.daemon = True
        self.data_recv_thread.start()

        self.send_list_lock = threading.Lock()

    def encode_ops(self) -> bytes:
        res = bytes()
        op_seq_num = self.seq_num
        for op in self.op_send_list:
            if op_seq_num >= self.send_until:
                break
            if len(res) + op.length >= gl.MAX_PACKET_SIZE - SEQ_INFO_LEN:
                break
            op_seq_num += 1
            res += op.encode()
        return res

    def decode_ops(self, data:bytes, seq_num:int):
        #TODO some sort of handling for malformed packets (discard) (need some detection in the Operation.from_num)
        i = 0
        seq_num_counter = seq_num
        while i < len(data):
            num = data[i]
            op = ops.Operation.from_num(num, data[i:])

            if seq_num_counter >= self.ack_num:
                if op.priority_op:
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
        #repeating ack
        if ack_num <= self.seq_num:
            return

        with self.send_list_lock:
            ack_op_count = ack_num - self.seq_num
            #FIXME is this actually better than using a list (instead of deque) and copying using [ack_op_count:]
            for i in range(0, ack_op_count):
                try:
                    self.op_send_list.popleft()
                except IndexError:
                    print('Connection desync with: ', self.address)
                    self.close()
                    return

            self.seq_num = ack_num

    def handle_incoming(self, data:bytes):
        seq_num, is_ack = self.decode_sync_info(data)

        if is_ack:
            self.handle_incoming_ack(seq_num)
        else:
            self.decode_ops(data[SEQ_INFO_LEN:], seq_num)
            while not self.net_op_recv_list.empty():
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

    def handle_all(self):
        while not self.op_recv_list.empty():
            self.op_recv_list.get().handle(self)

    def send_new_outgoing(self):
        self.send_until = self.seq_num + len(self.op_send_list)
        self.resend_new_outgoing()

    def resend_new_outgoing(self):
        if self.send_until <= self.seq_num:
            return
        gl.sock.sendto(crc.add_crc(self.new_outgoing()), self.address)
        self.reset_timer()

    def send_new_ack(self):
        gl.sock.sendto(crc.add_crc(self.new_outgoing_ack()), self.address)

    def recv_packet(self, data):
        if data is None:
            # noinspection PyTypeChecker
            self.data_recv_queue.put(data)
        #FIXME double crc check
        elif crc.valid_crc(data):
            self.data_recv_queue.put(crc.remove_crc(data))

    def close(self):
        self.closed = True
        print('Closing connection with: ', self.address)
        #FIXME clear queue first? otherwise all previous ops will be handled before thread closes :(
        self.recv_packet(None)
        gl.events.append(('DISCONNECT', self.address))
        try:
            del gl.connections[self.address]
        except KeyError:
            pass

    def reset_timer(self):
        if self.closed:
            return
        try:
            self.resend_timer.cancel()
        except AttributeError:
            pass
        self.resend_timer = threading.Timer(RESEND_TIMEOUT, handle_resend, (self,))
        self.resend_timer.start()


    #incoming data      safe
    #incoming ack       affects sender list and seq_num
    #outgoing data      uses sender_list and seq_num
    #outgoing ack       safe

def data_recv_thread(c:Connection):
    while True:
        try:
            data = c.data_recv_queue.get(timeout=CONN_TIMEOUT)
            if data is None:
                return
            c.handle_incoming(data)

            if not c.knows_peer:
                print('Received bad connection request from ', c.address)
                c.close()
                return

        except queue.Empty:
            c.close()
            return

def handle_resend(c:Connection):
    if c.closed:
        return
    if c.seq_num < c.send_until:
        c.resend_new_outgoing()

def connect_to(address:tuple, conn_id:int, player_name:str) -> Connection:
    address = hlp.sanitize_address(address)
    if address in gl.connections:
        raise Exception("Address already in connections list")

    print('Connecting to: ', address)

    self = Connection(address)
    #FIXME mutex on this list???
    gl.connections[address] = self
    self.conn_id = conn_id
    self.player_name = player_name
    self.knows_peer = True
    gl.events.append(('CONNECT', address))
    self.add_op(ops.PlayerInfo.my_info())
    self.send_new_outgoing()
    return self