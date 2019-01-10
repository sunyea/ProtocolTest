#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : SMTP.py
# @Author: Liaop
# @Date  : 2019-01-10
# @Desc  : smtp协议测试


import socket
import base64

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('smtp.exmail.qq.com', 25))
print('链接smtp服务器')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'HELO smtp.exmail.qq.com\r\n')
print('查询扩展功能')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'AUTH LOGIN\r\n')
print('用户登录')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

uid = 'liaopeng@kuaidanshou.com'
uid = base64.b64encode(uid.encode('utf8'))+b'\r\n'
s.send(uid)
print('提交账号')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

uid = '754607Lp'
uid = base64.b64encode(uid.encode('utf8'))+b'\r\n'
s.send(uid)
print('提交密码')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'MAIL FROM: liaopeng@kuaidanshou.com\r\n')
print('发送者邮箱')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'RCPT TO: 7192506@qq.com\r\n')
print('接受者邮箱')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'DATA\r\n')
print('准备发送内容')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'line1\r\n')
s.send(b'line2\r\n')
s.send(b'line3\r\n')
s.send(b'\r\n.\r\n')
print('发送内容')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))

s.send(b'QUIT\r\n')
print('退出')
rt = s.recv(1024)
print('反馈：{}'.format(rt.decode('utf-8')))