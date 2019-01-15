#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File  : RawSocket.py
# @Author: Liaop
# @Date  : 2019-01-15
# @Desc  : 原生socket测试

import os
import time
import socket
import struct
import random


def SendPacketData(Buffer=None, DestIP='127.0.0.1', DestPort=0):
    if Buffer is None:
        return False
    try:
        Socket = socket.socket(socket.AF_INET, socket.SOCK_RAW)
        Socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        Socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 2000)
    except:
        Socket.close()
        return False

    try:
        Socket.sendto(Buffer, 0, (DestIP, DestPort))
    except:
        Socket.close()

    return True


def SetPacketAddress(Number=1):
    return ['.'.join(['{}'.format(random.randint(1, 0xFF)) for i in range(0, 4)]) for n in range(0, Number)]


def SetPacketData(Length=32):
    return ''.join(['{}'.format(chr(random.randint(0, 255))) for n in range(Length)])


def SetPacketCheckSum(Buffer=None):
    if Buffer is None:
        return False
    if len(Buffer) % 2:
        Buffer += b'0'
    return ~sum([(ord(Buffer[n+1]) << 8) + ord(Buffer[n]) for n in range(0, len(Buffer), 2)])


def SynSendInit(DestIP='127.0.0.1', DestPort=80):
    IpHdrLen = 20
    TcpHdrLen = 20

    IpVerLen = (4<<4|int(IpHdrLen/4))
    IpTotal_len = socket.htons(IpHdrLen + TcpHdrLen)

    IpDestIP = struct.unpack('i', socket.inet_aton(DestIP))[0]
    IpSourceIP = struct.unpack('i', socket.inet_aton(SetPacketAddress()[0]))[0]

    TcpSport = socket.htons(random.randint(1024, 65000))
    TcpDport = socket.htons(DestPort)

    TcpLenres = (int(TcpHdrLen/4) << 4|0)
    TcpSeq = socket.htonl(int(time.time()))

    Buffer = struct.pack('LLBBHHHLLBBHHH', IpSourceIP, IpDestIP, 0, socket.IPPROTO_TCP, socket.htons(TcpHdrLen), TcpSport, TcpDport, TcpSeq, 0, TcpLenres, 2, socket.htons(8192), 0, 0)
    TcpChecksum = SetPacketCheckSum(Buffer)

    Buffer = struct.pack('BBHHHBBHLL', IpVerLen, 0, IpTotal_len, 1, 0x40, 255,
                         socket.IPPROTO_TCP, 0, IpSourceIP, IpDestIP)
    IpChecksum = SetPacketCheckSum(Buffer)

    tcpcsp = struct.pack('L', TcpChecksum)
    ipcsp = struct.pack('L', IpChecksum)

    return struct.pack('BBHHHBBHLLHHLLBBHHH', IpVerLen, 0, IpTotal_len, 1, 0x40, 255, socket.IPPROTO_TCP,
                       (ord(ipcsp[1]) << 8) + ord(ipcsp[0]), IpSourceIP, IpDestIP,
                       TcpSport, TcpDport, TcpSeq, 0, TcpLenres, 2, socket.htons(8192),
                       (ord(tcpcsp[1]) << 8) + ord(tcpcsp[0]), 0)


def SynSendMain(DestIP='127.0.0.1', DestPort=80):
    return SendPacketData(SynSendInit(DestIP, DestPort), DestIP, DestPort)

if __name__ == '__main__':
    SynSendMain()