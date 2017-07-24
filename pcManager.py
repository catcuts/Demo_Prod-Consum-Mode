# -*- coding:utf-8 -*-

# 概述：管理 生产者-消费者 模式
# 工作：
#       1.  开启 生产者-消费者 模式
#       2.  关闭 生产者-消费者 模式

import twisted
from twisted.internet import reactor
from twisted.internet.defer import Deferred

class pcManager(object):

    def __init__(self):
        d = defer.Deferred()
        d.addCallback(consumer)
        reactor.callInThread(producer, d.callback, d.errback, 'data')  

    def startpc(self):
        reactor.run() 

    def stoppc(self):
        reactor.stop()

    def producer(callback, errback, data):  # 生产者
        callback('test')

    def consumer(self, data):  # 消费者
        print('result: %s' %data)

    
     

