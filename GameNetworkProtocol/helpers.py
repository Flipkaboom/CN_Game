#FIXME inefficient?
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