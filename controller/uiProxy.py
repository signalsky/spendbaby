"""
Created on 2012-4-28
@author: Yang.Guozheng
"""

import os
import socket
import simplejson
import time
import traceback
from threading import Thread
from log import initLog

class UiMessage(object):
    """
    Used to communicate between controller and qt.
    Or exchange message controller ckc queue.
    """
    def __init__(self, *args, **kwargs):
        self.type = kwargs.get('type')
        self.cid = kwargs.get('cid')
        self.param_info = kwargs.get('param_info')
        self.args = args
        self.wid = ""
    
    def loads(self, data):
        """
        Deserialize 's' (a 'str' or 'unicode' instance containing a JSON
        document) to a Python object.
        
        @type data: {string}
        @param data: json string
        """
        params = simplejson.loads(data)
        self.type = params.get('type') or 'EVENT'
        self.cid = params['cid']
        self.wid = params['wid']
        self.param_info = params.get('param_info') or {}
        self.args = tuple(params.get('args') or ())
    
    def dumps(self):
        """
        Serialize 'self' to a JSON formatted 'str'.
        
        @rtype: {string}
        @return: json string
        """
        params = {}
        params['type'] = self.type
        params['cid'] = self.cid
        params['wid'] = self.wid
        params['param_info'] = self.param_info
        params['args'] = self.args
        return simplejson.dumps(params)
    
    def __str__(self):
        return "{'type':%s, 'wid':%s, 'cid':%s, 'param_info':%s, 'args':%s}" % (self.type, self.wid, self.cid,  self.param_info, self.args)

class UiSocket(object):
    def __init__(self):
        self.port = 49527
        self.sock = None
        self._msgLen = 0
        self._msg = ""
        self._buffer = ""
    
    def open(self):
        pass
    
    def close(self):
        pass
    
    def recvMessage(self):
        if self._msg:
            msg = self._parseTcpStream()
            if msg:
                return msg
        
        while True:
            data = self.sock.recv(4096)
            if not data:
                raise RuntimeError("socket connection broken")
            else:
                msg = self._parseTcpStream(data)
                if msg:
                    return msg
    
    def sendMessage(self, message):
        data = message.dumps()
        msg = "%s\n%s" % (len(data), data)
        self.sock.sendall(msg)
        
    
    def _parseTcpStream(self, data=""):
        self._buffer = ""
        self._msg += data
        
        if self._msgLen == 0 and self._msg:
            try:
                i = self._msg.index('\n')
                self._msgLen = int(self._msg[:i])
                self._msg = self._msg[i+1:]
            except:
                # packet is empty, try next time
                pass
        
        if self._msg and self._msgLen > 0 and len(self._msg) >= self._msgLen:
            self._buffer = self._msg[:self._msgLen]
            self._msg = self._msg[self._msgLen:]
            self._msgLen = 0
        
        if self._buffer:
            message = UiMessage()
            message.loads(self._buffer)
            return message
        else:
            return None

class UiServer(UiSocket):
    def __init__(self):
        super(UiServer, self).__init__()
    
    def open(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    
    def close(self):
        if self.server:
            self.server.close()
        if self.sock:
            self.sock.close()
    
    def listen(self):
        self.server.bind(('127.0.0.1', self.port))
        self.server.listen(1)
    
    def accept(self):
        self.sock, self.addr = self.server.accept()

class UiClient(UiSocket):
    def __init__(self):
        super(UiClient, self).__init__()
    
    def open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def close(self):
        if self.sock:
            self.sock.close()
    
    def connect(self):
        self.sock.connect(('127.0.0.1', self.port))
        
class UiProxy(object):
    """
    classdocs
    """
    (RUNNING, STOP) = range(2)
    
    def __init__(self, inputQ, outputQ):
        self.inputQ = inputQ
        self.outputQ = outputQ
        self.guiReady = False
        self._state = UiProxy.RUNNING
        self.runningThread = []
        self.server = UiServer()
        self.log = initLog("uiproxy")
    
    def initServer(self):
        self.log.info(" open server port and listen. ".center(90, '='))
        try:
            self.server.open()
            self.server.listen()
        except:
            self.log.error('server socket init failed:\n%s' % traceback.format_exc())
            raise
    
    def start(self):
        self.log.info("start working threads.")
        for t in (self._recv, self._send):
            ti = Thread(target=t)
            ti.setDaemon(True)
            ti.start()
            self.runningThread.append(ti)
    
    def stop(self):
        self._state = UiProxy.STOP
        self.server.close()
        for i in self.runningThread:
            i.join()
    
    def _recv(self):
        try:
            self.server.accept()
            self.guiReady = True
            
            while self._state == UiProxy.RUNNING:
                msg = self.server.recvMessage()
                self.log.info("Server get command: %s" % repr(msg))
                self.process(msg)
        except:
            if self._state == UiProxy.RUNNING:
                self.log.error('server get command: %s' % self.server._buffer)
                self.log.error('server recv failed:\n%s' % traceback.format_exc())
                self._alertSocketError()
    
    def _send(self):
        try:
            while self._state == UiProxy.RUNNING:
                message = self.outputQ.get()
                self.log.info("send message: %s" % message)
                self.server.sendMessage(message)
        except:
            if self._state == UiProxy.RUNNING:
                self.log.error('server send failed:\n%s' % traceback.format_exc())
                self._alertSocketError()
    
    def _alertSocketError(self):
        message = UiMessage(type='SOCKERROR')
        self.outputQ.put(message)
        self.inputQ.put(message)
#        self.server.close()
    
    def process(self, message):
        self.log.info("recv message: %s" % message)
        self.inputQ.put(message)

