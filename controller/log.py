"""
Created on 2012-4-28
@author: Yang.Guozheng
"""

import os
import time
import logging
import logging.handlers
import traceback


def initLog(handleName, fileName="", debug=False, rotate='size'):
    """
    New logger rotate
    @param handleName: The logger name, and log file name as deafult.
    @param fileName: The log file path, set as handleName as default if it's empty.
    @param debug: Logging debug infomation.
    @param rotate: Log file rotate by 'date' or 'size'.
    """
    type = True
    log = SpandLog(type, handleName, fileName, debug, rotate)    
    return log

def getLogger(handleName):
    type = False
    log = SpandLog(type, handleName)    
    return log
        

class SpandLog(object):        
    def __init__(self, type, handleName, fileName="", debug=False, rotate="size", level=logging.DEBUG):
        
        self.record_time = 0
        if not type:
            self.log = logging.getLogger(name=handleName)
        else :
            self.log = logging.getLogger(name=handleName)
            self.level = level
            if not fileName:
                fileName = handleName
            logfile = os.path.join("./log/%s.log" % fileName.lower())
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(thread)d %(message)s')
            
            if rotate == False:
                handle = logging.FileHandler(logfile)
                handle.setFormatter(formatter)
                self.log.addHandler(handle)
            else:
                if rotate == 'size':
                    rotateHandle = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024*1024*5, backupCount=5)
                elif rotate == 'date':
                    rotateHandle = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight', backupCount=5)
                else:
                    rotateHandle = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024*1024*5, backupCount=5)
                rotateHandle.setFormatter(formatter)
                self.log.addHandler(rotateHandle)

            if debug:
                self.log.setLevel(logging.DEBUG)
            else:
                self.log.setLevel(logging.INFO)
            
    def getlog(self):
        return self.log
 
    def info(self, log):
        self.log.info(log)       

    def error(self, log):
        self.log.error(log)
         
    def debug(self, log):
        self.log.debug(log)

    def warning(self, log):
        self.log.warning(log)
        
