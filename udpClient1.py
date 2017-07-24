# -*- coding:utf-8 -*-
import socket
from ipManager import ipAddress
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'Michael', b'Tracy', b'Sarah', b'Catcuts', b'Adam', b'Bob', b'Lucy', b'HanMeimei', b'LiLei']:
    # 发送数据:
    s.sendto(data, (ipAddress, 9999))
    # 接收数据:
    print(s.recv(1024).decode('utf-8'))  # 如果服务器没有发回数据，则客户端卡在此处，不会发送下一个数据
s.close()