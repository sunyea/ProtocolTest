#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : HTTP.py
# @Author: Liaop
# @Date  : 2019-01-10
# @Desc  : 测试http协议
'''
GET     请求获取Request-URI所标识的资源

POST    在Request-URI所标识的资源后附加新的数据

HEAD    请求获取由Request-URI所标识的资源的响应消息报头

PUT     请求服务器存储一个资源，并用Request-URI作为其标识

DELETE  请求服务器删除Request-URI所标识的资源

TRACE   请求服务器回送收到的请求信息，主要用于测试或诊断

CONNECT 保留将来使用

OPTIONS 请求查询服务器的性能，或者查询与资源相关的选项和需求

'''

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('192.168.100.71', 80))

s.send(b'GET / HTTP/1.1\r\nHost: 192.168.100.71\r\n\r\n')

rt = s.recv(1024)
while rt:
    print(rt.decode('utf-8'))
    rt = s.recv(1024)
