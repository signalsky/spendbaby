"""
Created on 2012-4-28
@author: Yang.Guozheng
"""

import sys
import traceback

def createDaemon():
    try:
        if os.fork() > 0:
            sys.exit(0)
    except OSError, error:
        print 'fork #1 failed: %d (%s)' % (error.errno, error.strerror)
        sys.exit(1)
    
    # it separates the son from the father
    #os.chdir(path)
    os.setsid()
    os.umask(23)
    
    try:
        pid = os.fork()
        if pid > 0:
            msg = 'Daemon PID %d' % pid
            print msg
            sys.exit(0)
    except OSError, error:
        print 'fork #2 failed: %d (%s)' % (error.errno, error.strerror)
        sys.exit(1)

        