import os

def str_to_hex(str, gap):
    list_hex = []
    if not len(str) % gap:
        for i in range(0, len(str), gap):
            list_hex.append(int(str[i : i+2], 16))
    else:
        print 'ERROR'
    return list_hex

def calc_checksum(buf):
    ret = 0
    for i in range(len(buf)):
        ret += buf[i]
    return ret & 0xff
