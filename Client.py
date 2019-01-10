#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : Client.py
# @Author: Liaop
# @Date  : 2019-01-09
# @Desc  : Socket测试客户端

import socket
import time
import threading


def client(id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.100.69', 9999))
    print(s.recv(1024).decode('utf-8'))

    while True:
        time.sleep(5)
        s.send(('client {} message'.format(id)).encode('utf-8'))


for i in range(10240):
    t = threading.Thread(target=client, args=(i,))
    t.start()