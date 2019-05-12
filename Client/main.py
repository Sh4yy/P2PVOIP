from api import API
from puncher import UDPPunch
import socket
from call import CallAPI
from random import randint

name = input("name > ")

ip, port = "0.0.0.0", randint(5000, 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((ip, port))

puncher = UDPPunch(("158.69.1.114", 5700))
api = API("158.69.1.114:5701", puncher)
try:
    api.register(name, "1234")
except:
    pass
api.login(name, "1234")
api.update_my_address(sock)
print(api.my_address(sock))
call = CallAPI(api, name, sock)
call.idle()
