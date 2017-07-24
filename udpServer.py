# -*- coding:utf-8 -*-

# 概述：udp 服务器，管理 udp 连接、关闭、接收、发送
# 工作：
#     1.  收到数据后 -> 开启生产者线程
# 注释：
#     1.  UDP 没有连接的概念，因此它的协议 DatagramProtocol 不像 TCP 中的协议 Protocol ，有 connectionMade 方法

import os
import sys
import time
import twisted
from twisted.internet.protocol import DatagramProtocol
from utils.printl import printl
from config.base import logfilePath
from Queue import PriorityQueue
from twisted.internet import reactor

class udpServer(DatagramProtocol):

    def __init__(self):
        self.log = ''
        self.caches = {}

    def startProtocol(self):  # start updServer
        pass

    def stopProtocol(self):  # stop udpServer
        pass

    def datagramReceived(self, data, client):
        
        caches = self.caches

        cache = caches.get(client,None)  # 从缓存区字典中取得对应客户端的缓存区
        if cache is None:  # 如果不存在该缓存区
            cache = {  # 则创建一个
                'queue': PriorityQueue(),
                'join_time': time.time(),
                'last_remain': b''
            }
            caches[client] = cache  # 并保存到缓存区字典
            reactor.callInThread(producer, client)  # 同时开启一个消费者线程，向 client 对应的队列取得数据

        queue = cache["queue"]  # 如果存在该缓存区，则取得对应的缓存队列
        data = splitUDPpackage(data)  # 对数据进行拆包，拆包后 data 获得三个属性： 本体body, 余体remain, 优先级priority
        queue.put(data.body, data.priority)  # 将数据本体投入缓存队列（非阻塞式）
        cache['last_remain'] = data.remain  # 将数据余体放入缓存相应位置


    def savedata(client):
        cache=caches.get(client,None)
        queue=cache["queue"]
        datas=ByteIO()
        datalen=queue.qsize()
        while True:
            cur_time=time.time
            if cur_time-time>10:
                break;


        data=queue.get(data)
        datas.write(data)

        with open("ffff.dat","wb") as f
            f.write

        del cache


    def splitUDPpackage(self, data)
        return data