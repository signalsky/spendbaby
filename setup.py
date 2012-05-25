"""
Created on 2012-4-28
@author: Yang.Guozheng
"""

import sys
import os
USAGE = "Usage: python setup.py [start|stop|restart]"

if __name__ == "__main__":
    clen = len(sys.argv)
    if clen > 2:
        print USAGE
        sys.exit(1)
    elif clen == 2 and (sys.argv[1] != "start" and sys.argv[1] != "stop"):
        print USAGE
        sys.exit(1)
    elif clen == 2 and sys.argv[1] == "stop":
        os.system("pkill -f gui.py")
        os.system("pkill -f main.py")
    else:
        path = os.getcwd()
        main_file = os.path.join(path,"controller/main.py")
        gui_file = os.path.join(path,"viewer/gui.py")
        log_file = os.path.join(path,"tmp/controller.log")
        log_gui = os.path.join(path,"tmp/qt.log")
        #os.system("chmod +x " + main_file)
        #os.system("chmod +x " + gui_file)
        os.system("python " + main_file + " > " + log_file + "  2>&1 &")
        os.system("python " + gui_file + " -display :0 -style windows > " + log_gui + "  2>&1 &")


    