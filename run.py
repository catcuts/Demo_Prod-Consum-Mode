# -*- coding:utf-8 -*-

# 概述：运行整个工程
# 工作：
# 	1.  启动 udpServer
# 	2.  启动 

import os
import twisted
from twisted.internet import reactor
from udpServer import udpServer
from utils.printl import printl
from config.base import logfilePath

if __name__ == "__main__":
	port = '9999'
	logfilePath = os.path.join(os.getcwd(), 'data\\log\\default_log.txt')
	try:
		port = argv[1]
		logfilePath = argv[2]
	except:
		pass

	log = 'start linstening UPD on port ' + port
	printl(log, logfilePath, toConsole=True, reset=True)

	reactor.listenUDP(int(port), udpServer())
	reactor.run()