#!/usr/bin/python
"""
Created on 2012-5-24
@author: Yang.Guozheng
"""
import os
import sys
import threading
import simplejson as json
from PyQt4 import QtCore, QtGui
sys.path.append(os.getcwd()+"/controller")
from log import initLog
from uiProxy import UiClient,UiMessage
from windows import Ui_MainWindow

gui_log = initLog("qt_gui", debug=True)

class qMessage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gui_log
        self.log = gui_log
        try:
            self.socketq = UiClient()
            self.socketq.open()
            self.socketq.connect()
            self.log.info(" ============================== gui connect successfully. ==============================")
        except Exception, ex:
            self.log.error('[socketQuery] [Error] Can not connect: %s' %ex)
            raise
        self.sd = self.socketq.sock
        self.msg_buffer = ""

    def run(self):
        self.log.info(" ============================== start receive message. ==============================")
        test_msg = UiMessage("{'type':'test', 'wid':'none', 'cid':'none', 'param_info':{}, 'args':()}")
        self.socketq.sendMessage(test_msg)
        while True:
            self.msg_buffer = self.socketq.recvMessage()
            self.log.debug(self.msg_buffer)
                
    def send(self, data):
        try:
            data = json.dumps(data)
            self.socketq.sock.send(str(len(data))+"\n")
            self.socketq.sock.send(data)
            self.log.info('Sending data: %s' %data)
        except Exception, ex:
            self.log.error('[socketQuery] [Error] Can not send: %s;\n Send data: %s' %(ex,data))

    def deinit(self):
        self.socketq.close()
        
if __name__ == "__main__":
    print " ============================== start gui. =============================="
    msg = qMessage()
    msg.start()
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


