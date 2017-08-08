# -*- coding:utf-8 -*-

# 概述：udp 服务器，管理 udp 连接、关闭、接收、发送
# 工作：
#     1.  收到数据后 -> 开启生产者线程
# 注释：
#     1.  UDP 没有连接的概念，因此它的协议 DatagramProtocol 不像 TCP 中的协议 Protocol ，有 connectionMade 方法
#     2.  一个连接（或客户端）对应一个线程
# 考虑：
#     1.  并发 <- 多线程 ( 一个连接一个线程 )
#     2.  粘包 <- 拆包 ( splitUDPpackage )
#     3.  保存 <- avi格式 ( saveData )
#     4.  信令协商 <- 开始 中断 结束 ( .. )

import os
import sys
import time
import twisted
from twisted.internet.protocol import DatagramProtocol
from utils.printl import printl
from config.base import logfilePath
from Queue import PriorityQueue
from twisted.internet import reactor

caches = {}
sessions = {}

class VideoSession():

    def __init__(self, client):
        self.client = client

        cache = caches.get(client, None)  # 从缓存区字典中取得对应客户端的缓存区
        if cache is None:  # 如果不存在该缓存区
            cache = {  # 则创建一个
                'queue': PriorityQueue(),  # 队列
                'join_time': time.time(),  # 缓存区生成时间
                'last_remain': b'',  # 上一个 UDP 包的余体
                'full': 50 * 1024 * 1024,  # 单位 byte 保存阈值（缓存满了就保存）
                'doubt': 100 * 1024 * 1024,  # 单位 byte 怀疑阈值
                'idle_time': 'unset',  # 空闲时间点
                'timeout': 10,  # 单位 s  # 空闲超时时间
                'size': 0  # 单位 byte 缓存区大小
            }
            caches[client] = cache  # 并保存到缓存区字典
        self.cache = cache

        self.startSession()

    def startSession(self):
        printl('Caller: start a session for client: %s' %(self.client,), logfilePath)
        reactor.callInThread(self.consumeData)  # 同时开启一个消费者线程，向 client 对应的队列取得数据

    def stopSession(self):
        printl('Caller: stop a session for client: %s' %(self.client,), logfilePath)
        del cache[self.client]
        del sessions[self.client]

    def receiveData(self, data):  # 生产者
        printl('Producer: start receiving data from client: %s' %(self.client,), logfilePath)

        cache = self.cache

        cache['idle_time'] = time.time()  # 复位空闲时间点
        q = cache['queue']  # 如果存在该缓存区，则取得对应的缓存队列
        data = self.splitUDPpackage(data, 'b')  # 对数据进行拆包，拆包后 data 获得三个属性： 本体 body, 余体 remain, 优先级 priority, 大小 size
        q.put((data['priority'], cache['last_remain'] + data['body']))  # 将数据本体投入缓存队列（非阻塞式）
        cache['last_remain'] = data['remain']  # 将数据余体放入缓存相应位置
        cache['size'] += data['size']  # 计算缓存区新的大小

    def consumeData(self):  # 消费者
        cache = self.cache
        client = self.client
        q = cache['queue']
        printl('Consumer: start observing queue of client: %s' %(client,), logfilePath)
        while True:  # 等待数据接收完毕，则退出等待，一次性读取整个缓存队列  
            # 等待期间，应防止缓存区溢出 <- 达到消费阈值则及时消费 + 达到怀疑阈值则及时检查并开启新消费线程
            # 退出条件 <- 空闲了 10 秒
            current_time = time.time()  # 当前时间点
            if cache['idle_time'] != 'unset' and (current_time - cache['idle_time'] > 10):  # 如果 当前时间点 - 空闲时间点 > 10 秒 前提是已经设置了为空时间点
                printl('Consumer: stop waiting for client: %s reason: overtime 10 sec' %(client,), logfilePath)
                break  # 退出等待，开始保存

            # 达到怀疑阈值则开启新消费线程（怀疑线程异常退出）
            if cache['size'] >= cache['doubt']:
                printl('Consumer: restart a session for client: %s\n\treason: consumeData threading might be dead' %(client,), logfilePath)
                self.startSession(client)

            # 达到保存阈值则及时保存
            if cache['size'] >= cache['full']:
                printl('Consumer: stop waiting for client: %s\n\treason: queue is full' %(client,), logfilePath)
                self.saveData(q)

        self.saveData(q)

        self.stopSession()

    def splitUDPpackage(self, data, encode):
        printl('Producer: start splitting UDP package from client: %s' %(self.client,), logfilePath)
        # do splitting
        printl('Producer: finish splitting UDP package from client: %s' %(self.client,), logfilePath)
        return {
            'body': data,  # 要转成二进制流
            'remain': b'',
            'priority': 1,
            'size': 24
        }

    def saveData(self, q):
        printl('Consumer: start saving data from client: %s' %(self.client,), logfilePath)

        data_filedir = os.getcwd() + '\\data\\video'
        if not os.path.isdir(data_filedir):
            os.makedirs(data_filedir)
        data_filepath = os.path.join(data_filedir, 'video_' + str(self.cache['join_time']) + '.dat')
        if not os.path.isfile(data_filepath):
            open_method = 'wb'
        else:
            open_method = 'ab'
        with open(data_filepath, open_method) as f:
            data_len = q.qsize()
            for i in range(data_len):
                data = q.get()[1]
                print('\tdata: %s' %data)
                f.write(data)
        printl('Consumer: saved data from client: %s in file: %s' %(self.client, data_filepath), logfilePath)

class VideoServer(DatagramProtocol):

    def __init__(self):
        pass

    def startProtocol(self):  # start updServer
        pass

    def stopProtocol(self):  # stop udpServer
        pass

    def datagramReceived(self, data, client):
        printl('from client %s received %r' % (client, data), logfilePath)
        vs = self.getSession(client)  # 获取客户端对应的会话
        vs.receiveData(data)  # 接收数据到这个会话

    def getSession(self, client):
        if not sessions.get(client, None):  # 如果该客户端还未建立会话
            session = VideoSession(client)  # 则建立一个新会话
            sessions[client] = session  # 并保存
        return sessions[client]  # 返回这个会话对象