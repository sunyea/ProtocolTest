#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : Server.py
# @Author: Liaop
# @Date  : 2019-01-09
# @Desc  : socket链接服务端

import socket
import time
import threading

def tcplink(sock, addr):
    print('Accept new connection from {}'.format(addr))
    sock.send(b'response')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        # sock.send(('responsed: {}'.format(data.decode('utf-8'))).encode('utf-8'))
        print('{} get msg:{}'.format(len(c_list), data.decode('utf-8')))
    sock.close()
    print('Connection from {} closed'.format(addr))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.100.69', 9999))
s.listen(32)
print('等待客户端连接...')
c_list = list()
while True:
    sock, addr = s.accept()
    c_list.append(sock)
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
