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

def decodeall(buff):
    s = None
    try:
        s = buff.decode('utf-8')
        return s
    except:
        pass
    try:
        s = buff.decode('unicode')
        return s
    except:
        pass
    try:
        s = buff.decode('gb2312')
        return s
    except:
        pass
    return s


def CreateSocket():
    try:
        Socket = socket.socket(socket.AF_INET, socket.SOCK_RAW)
        Socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        Socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, 2000)
        return Socket
    except Exception as e:
        Socket.close()
        print('创建socket失败：{}'.format(e))
        return None


def GetIPHeader(SourceIP, DestIP, CheckSum=0):
    '''
    获取IP首部
    :param SourceIP: 源地址
    :param DestIP: 目的地址
    :return:
    '''
    try:
        # 4 版本
        version = 4
        # 4 首部长度
        head_len = 5
        ver_head_len = (version << 4)+head_len

        # 8 服务类型
        server = 0
        # 16 总长度
        tot_len = 20 + 20
        # 16 标识
        id = random.randint(18000, 65535)
        # 3 标志
        flag = 0
        # 13 片偏移
        offset = 0
        flag_offset = (flag << 13)+offset

        # 8 生存期
        ttl = 255
        # 8 协议
        protocol = socket.IPPROTO_TCP
        # 16 首部验证和
        check_sum = CheckSum
        # 32 源地址
        source_ip = socket.inet_aton(SourceIP)
        # 32 目的地址
        dest_ip = socket.inet_aton(DestIP)

        ip_header = struct.pack('BBHHHBBH4s4s', ver_head_len, server, tot_len, id, flag_offset
                                , ttl, protocol, check_sum, source_ip, dest_ip)
        return ip_header
    except Exception as e:
        print('Error : {}'.format(e))
        return None


def GetTcpHeader(SourcePort, DestPort, CheckSum=0):
    '''
    获取TCP首部
    :param SourcePort:源端口
    :param DestPort:目标端口
    :return:
    '''
    try:
        # 16 源端口
        source_port = socket.htons(SourcePort)
        # 16 目的端口
        dest_port = socket.htons(DestPort)
        # 32 序号
        seq = 0
        # 32 确认号
        ack_seq = 0
        # 4 头部长度
        head_len = 5
        # 6 保留位
        reserve = 0
        # 6 TCP标志位
        fin = 0
        syn = 1
        rst = 0
        psh = 0
        ack = 0
        urg = 0
        tcp_flag = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)
        head_flag = (head_len << 12) + (reserve << 6) + tcp_flag

        # 16 窗口大小
        window = socket.htons(8192)
        # 16 检验和
        check_sum = CheckSum
        # 16 紧急指针
        urg_ptr = 0

        tcp_header = struct.pack('HHIIHHHH', source_port, dest_port, seq, ack_seq, head_flag
                                 , window, check_sum, urg_ptr)
        return tcp_header

    except Exception as e:
        print('Error : {}'.format(e))
        return None


def GetCheckSum(Header=None):
    '''
    获取校验和
    :param Header:
    :return:
    '''
    if Header is None:
        return None
    if len(Header) % 2:
        Header += b'0'
    try:
        all_sum = sum([(Header[n] << 8) + Header[n+1] for n in range(0, len(Header), 2)])
        l_word = all_sum & 0x0000FFFF
        h_word = all_sum >> 16
        check_sum = l_word + h_word
        check_sum2 = (~check_sum) & 0xFFFF
        return check_sum2
    except Exception as e:
        print('Error : {}'.format(e))
        return None


def GetIPPacket(SourceIP, SourcePort, DestIP, DestPort):
    '''
    获取IP包
    :param SourceIP:
    :param SourcePort:
    :param DestIP:
    :param DestPort:
    :return:
    '''
    # 构建TCP包
    try:
        tcp_packet = GetTcpHeader(SourcePort, DestPort)
        tcp_checksum = GetCheckSum(tcp_packet)
        if tcp_checksum is None:
            return None
        tcp_packet = GetTcpHeader(SourcePort, DestPort, tcp_checksum)
        if tcp_checksum is None:
            return None

        # 构建IP包
        ip_packet = GetIPHeader(SourceIP, DestIP)
        ip_checksum = GetCheckSum(ip_packet)
        if ip_checksum is None:
            return None
        ip_packet = GetIPHeader(SourceIP, DestIP, ip_checksum)
        if ip_checksum is None:
            return None

        return ip_packet + tcp_packet
    except Exception as e:
        print('Error : {}'.format(e))
        return None

def IPUnpacket(Buffer):
    ver_head_len, server, tot_len, id, flag_offset, ttl, protocol, check_sum, source_ip, \
    dest_ip = struct.unpack('!BBHHHBBH4s4s', Buffer[:20])
    head_len = ver_head_len & 0xF
    s_ip = socket.inet_ntoa(source_ip)
    d_ip = socket.inet_ntoa(dest_ip)
    print('head_size:{}, all_size:{}, id:{}, ttl:{}, source_ip:{}, dest_ip:{}'.format(head_len, tot_len
            ,id, ttl, s_ip, d_ip))
    if tot_len < 40:
        return None
    source_port, dest_port, seq, ack_seq, head_flag, window, check_sum, urg_ptr = struct.unpack('!HHIIHHHH'
                                                                                                ,Buffer[20:40])
    head_len2 = head_flag >> 12
    print('source_port:{}, dest_port:{}, seq:{}, ack_seq:{}, window:{}, head_len:{}'.format(source_port
                                                                , dest_port, seq, ack_seq, window, head_len2))
    if head_len == head_len2:
        buff = Buffer[40:]
        print('data:{}'.format(decodeall(buff)))


if __name__ == '__main__':
    sock = CreateSocket()
    SourceIP = '192.168.100.69'
    SourcePort = random.randint(1024, 65000)
    DestIP = '192.168.100.71'
    DestPort = 80
    buff = GetIPPacket(SourceIP, SourcePort, DestIP, DestPort)
    sock.sendto(buff, (DestIP, DestPort))
    while True:
        header, addr = sock.recvfrom(1024)
        if header:
            print('recv:{}'.format(addr))
            IPUnpacket(header)