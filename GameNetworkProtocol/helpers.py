import random

from . import globals as gl

def sanitize_ip(ip:str):
    if ip == '' or ip == '0.0.0.0' or ip == 'localhost':
        return '127.0.0.1'
    else:
        return ip

def sanitize_address(address:tuple):
    if address[0] == '' or address[0] == '0.0.0.0' or address[0] == 'localhost':
        return '127.0.0.1', address[1]
    else:
        return address

def random_drop_incoming():
    return random.randint(0,99) < gl.incoming_drop_chance

def random_drop_outgoing():
    return random.randint(0,99) < gl.outgoing_drop_chance