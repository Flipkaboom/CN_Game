POLYNOMIAL = "101111101"
PART_SIZE = 8

def add_crc(data: bytes) -> bytes:
    parts = list(split_sections(data, PART_SIZE))
    res = bytes()
    for part in parts:
        checksum = get_checksum(part)
        res += part
        res += checksum.to_bytes(1, 'big')
    return res

def remove_crc(data:bytes) -> bytes:
    parts = list(split_sections(data, PART_SIZE + 1))

    res = bytes()
    for part in parts:
        res += part[:-1]

    return res

def valid_crc(data:bytes) -> bool:
    parts = list(split_sections(data, PART_SIZE + 1))

    for part in parts:
        if get_checksum(part) != 0:
            return False

    return True

def split_sections(data:bytes, size:int):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def get_checksum(data:bytes) -> int:
    data += b'\x00'

    bindata_str = str()
    for byte in data:
        bindata_str += f'{byte:08b}'

    # print(bindata_str)

    bindata = list()
    for char in bindata_str:
        bindata += char

    # print(bindata)

    i = 0
    while i < len(bindata) - len(POLYNOMIAL) + 1:
        if bindata[i] == '0':
            i += 1
            continue

        for x in range(0, len(POLYNOMIAL)):
            if POLYNOMIAL[x] == '1':
                if bindata[i + x] == '1':
                    bindata[i + x] = '0'
                else:
                    bindata[i + x] = '1'

    checksum_bin = str()
    for bit in bindata[-(len(POLYNOMIAL) - 1):]:
        checksum_bin += bit
    return int(checksum_bin, 2)

