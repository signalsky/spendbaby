#!/usr/bin/python
"""
Created on 2012-4-28
@author: Yang.Guozheng
"""

import sys
import os
import traceback
from utils import createDaemon
from controller import Controller

def setup_work_environment():
    print "set up work environment."
    
        
if __name__ == "__main__":
    
    try:
        setup_work_environment()
        ctrl = Controller()
        ctrl.start()
        ctrl.mainloop()
    except:
        print >> sys.stderr, "Start program Failed!"
        print >> sys.stderr, traceback.format_exc()
    
    
