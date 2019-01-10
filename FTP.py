#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : FTP.py
# @Author: Liaop
# @Date  : 2019-01-10
# @Desc  : ftp协议测试

'''
FTP 每个命令都有 3 到 4 个字母组成，命令后面跟参数，用空格分开。每个命令都以 "\r\n"结束。

要下载或上传一个文件，首先要登入 FTP 服务器，然后发送命令，最后退出。这个过程中，主要用到的命令有 USER、PASS、SIZE、REST、CWD、RETR、PASV、PORT、QUIT。

USER: 指定用户名。通常是控制连接后第一个发出的命令。“USER gaoleyi\r\n”： 用户名为gaoleyi 登录。

PASS: 指定用户密码。该命令紧跟 USER 命令后。“PASS gaoleyi\r\n”：密码为 gaoleyi。

SIZE: 从服务器上返回指定文件的大小。“SIZE file.txt\r\n”：如果 file.txt 文件存在，则返回该文件的大小。

CWD: 改变工作目录。如：“CWD dirname\r\n”。

PASV: 让服务器在数据端口监听，进入被动模式。如：“PASV\r\n”。

PORT: 告诉 FTP 服务器客户端监听的端口号，让 FTP 服务器采用主动模式连接客户端。如：“PORT h1,h2,h3,h4,p1,p2”。
如得到 227 entering passive mode (h1,h2,h3,h4,p1,p2)，那么端口号是 p1*256+p2，ip 地址为h1.h2.h3.h4。

RETR: 下载文件。“RETR file.txt \r\n”：下载文件 file.txt。

STOR: 上传文件。“STOR file.txt\r\n”：上传文件 file.txt。

REST: 该命令并不传送文件，而是略过指定点后的数据。此命令后应该跟其它要求文件传输的 FTP 命令。“REST 100\r\n”：重新指定文件传送的偏移量为 100 字节。

QUIT: 关闭与服务器的连接。

'''

import socket
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('192.168.100.71', 21))
print('链接到ftp服务器')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'USER broker2\r\n')
print('发送用户名')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'PASS 147258369\r\n')
print('发送密码')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'PASV\r\n')
print('发送被动模式')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))
s_rt = rt.decode('utf-8')
x = re.search('\((.*?)\)', s_rt).group(1)
x = x.split(',')
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect(('{}.{}.{}.{}'.format(x[0], x[1], x[2], x[3]), int(x[4])*256+int(x[5])))

s.send(b'LIST\r\n')
print('获取文件列表')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))
while True:
    rt = s2.recv(1024)
    print(rt.decode('utf-8'), end='')
    if len(rt) < 1024:
        break
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))
s2.close()

s.send(b'PASV\r\n')
print('发送被动模式')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))
s_rt = rt.decode('utf-8')
x = re.search('\((.*?)\)', s_rt).group(1)
x = x.split(',')
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect(('{}.{}.{}.{}'.format(x[0], x[1], x[2], x[3]), int(x[4])*256+int(x[5])))

s.send(b'SIZE zk.sh\r\n')
print('发送获取文件zk.sh大小')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'RETR zk.sh\r\n')
print('获取文件zk.sh')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

rt = s2.recv(1024)
print('反馈2：{}'.format(rt.decode('utf-8')))