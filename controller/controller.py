"""
Created on 2012-4-28
@author: Yang.Guozheng
"""

import os
import sys
from Queue import Queue, Empty
from log import initLog
from uiProxy import UiProxy
from sysException import GuiSocketException

class Controller(object):
    def __init__(self):
        self.forms = {}
        self.log = initLog("controller", debug=True)        
        self.inputQ = Queue()
        self.outputQ = Queue()
        self.gs = GlobalSession()
        self.timeout = 60
        

    def start(self):      
        # open the port and wait gui connection
        self.ui = UiProxy(self.inputQ, self.outputQ)
        self.ui.initServer()
        self.ui.start()
        self.log.debug("ui proxy started.")

    def stop(self, status=0):
        self.log.info("exiting ui")
        self.ui.stop()
        sys.exit(status)
        
    def mainloop(self):
        self.log.debug("main loop in controller.")
        #self.stop()
        #return 
        while True:
            try:
                message = self.inputQ.get(timeout=self.timeout)
                if message.type == "SOCKERROR":
                    self.log.error("SOCKERROR")
                    self.stop()             
                else:                                            
                    self.log.debug(str(message))
            except Empty:
                self.onTimeout()

    def onTimeout(self):
        pass
    
class History(object):
    def __init__(self, formState, args, kwargs):
        self.formState = formState
        self.args = args
        self.kwargs = kwargs
    
    def __str__(self):
        return "%s:%s" % (self.formState, self.kwargs)
        
class GlobalSession(object):
    def __init__(self):
        self._history = []
        self.args = ()
        self.kwargs = {}
        self.work_path = os.getcwd()    
    
    def addHistory(self, formState):
        self._goback = False
        self._history.append(History(formState, self.args, self.kwargs))
    
    def resetHistory(self, formState):
        self._goback = False
        self._history.pop()
        self._history.append(History(formState, self.args, self.kwargs))
    
    def popHistory(self):
        self._goback = True
        try:
            # pop current form
            history = self._history.pop()
            # pop last form
            history = self._history.pop()
            self.args = history.args
            self.kwargs = history.kwargs
            
            return history.formState
        except IndexError:
            return ''
    
    def clearHistory(self):
        self._history = []     
        
