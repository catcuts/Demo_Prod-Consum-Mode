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
from Queue import Queue
from twisted.internet import reactor

caches={}


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




class udpServer(DatagramProtocol):

    def __init__(self):
        self.datas = []
        self.lastPort = ''
        self.log = ''

    def startProtocol(self):  # 其实就是 start updServer ，或许 class udpServer 改名 class updProtocol 会比较合适
        pass

    def stopProtocol(self):  # stop udpServer
        printl(self.log, logfilePath, toConsole=False)  # 记录而不打印控制台

    def _get_data_index(self,data)
        pass
        return data



    def datagramReceived(self, data, client):
        if port != self.lastPort:  # 如果端口和上一次不一样
            if self.log:
                printl(self.log, logfilePath, toConsole=False)  # 记录而不打印控制台
            self.lastPort = port  # 重置上次端口
            self.datas = []  # 清空数据
            sys.stdout.write('\n')  # 控制台换行重新输出

        cache=caches.get(client,None)
        if cache is None:
            cache={
                "queue":Queue(),
                "join_time":time.time()
                }
            caches[client]=cache
            reactor.callInThread(savedata,client)

        queue=cache["queue"]
        queue.put(data)


        

        time.sleep(1)  # 模拟数据处理所需时间

        self.datas.append(data)  # push data

        sys.stdout.write(' ' * 1 + '\r')  # 从头（\r）覆盖
        sys.stdout.flush()  # 暂时输出

        sys.stdout.write('from %s:%d received data: ' % (host, port))  # 不换行
        sys.stdout.write(', '.join(self.datas) + '\r')  # 从头（\r）覆盖
        sys.stdout.flush()  # 暂时输出

        self.log = ('from %s:%d received data: ' % (host, port)) + ', '.join(self.datas)

        self.transport.write(data+': mewo', (host, port))
