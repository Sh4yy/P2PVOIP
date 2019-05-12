import re
import struct

IP_REG = r'^([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}):([0-9]{1,5})$'
IP_RE = re.compile(IP_REG)


def byte2ip(byte):
    assert (len(byte) == 6)
    a, b, c, d, port = struct.unpack(">BBBBH", byte)
    return f"{a}.{b}.{c}.{d}:{port}"


def ip2byte(ip):
    a, b, c, d, port = [int(x) for x in IP_RE.match(ip).groups()]
    return struct.pack(">BBBBH", a, b, c, d, port)


