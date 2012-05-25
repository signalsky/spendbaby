from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

window_style = "QMainWindow {margin: 1px;border: 2px solid green;padding: 20px;\
border-image: url(viewer/image/background.jpg);background-position: center center;\
background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #707070, stop:0.4 #202020, stop:0.6 #505050, stop:1 #202020);\
background-origin: content;background-repeat: none;}"
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/viewer/logo.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        #MainWindow.setAutoFillBackground(True)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "SpendBabyV1.0", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setWindowFlags(MainWindow.windowFlags()  & ~QtCore.Qt.WindowMaximizeButtonHint)
        MainWindow.setStyleSheet(window_style)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.createMenus(MainWindow)
        self.createToolBars(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

    def createMenus(self, MainWindow):
        drawMenu = MainWindow.menuBar().addMenu("file")

    def createToolBars(self, MainWindow):
        drawToolBar = MainWindow.addToolBar("Draw");
        
