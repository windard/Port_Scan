# coding=utf-8

import sys
import socket
from PyQt4 import QtGui,QtCore
import threading
from Queue import Queue

ip2num = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])
num2ip = lambda x: '.'.join([str(x/(256**i)%256) for i in range(3,-1,-1)])

class GScan(QtGui.QWidget):
    def __init__(self):
        super(GScan,self).__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(600,400)
        self.center()
        self.setWindowTitle(u"GScan 端口扫描工具")
        self.setStyleSheet("QWidget{background-color:#ccc;}")
        self.grid = QtGui.QGridLayout(self)
        self.grid.setSpacing(10)

        self.host_start = QtGui.QLabel("host_start")
        self.host_start_edit = QtGui.QLineEdit(self)
        self.grid.addWidget(self.host_start, 0, 0)
        self.grid.addWidget(self.host_start_edit, 0, 1)
        self.connect(self.host_start_edit,QtCore.SIGNAL("textChanged(QString)"),self.host_start_change)

        self.host_end = QtGui.QLabel("host_end")
        self.host_end_edit = QtGui.QLineEdit(self)
        self.grid.addWidget(self.host_end, 0, 2)
        self.grid.addWidget(self.host_end_edit, 0, 3)

        self.port_start = QtGui.QLabel("port_start")
        self.port_start_edit = QtGui.QLineEdit(self)
        self.grid.addWidget(self.port_start, 1, 0)
        self.port_start_edit.setText(QtCore.QString(str(0)))
        self.grid.addWidget(self.port_start_edit, 1, 1)
        self.connect(self.port_start_edit,QtCore.SIGNAL("textChanged(QString)"),self.port_start_change)

        self.port_end = QtGui.QLabel("port_end")
        self.port_end_edit = QtGui.QLineEdit(self)
        self.grid.addWidget(self.port_end, 1, 2)
        self.port_end_edit.setText(QtCore.QString(str(512)))
        self.grid.addWidget(self.port_end_edit, 1, 3)

        self.thread = QtGui.QLabel("thread")
        self.thread_edit = QtGui.QLineEdit(self)
        self.thread_edit.setText(QtCore.QString(str(4)))
        self.grid.addWidget(self.thread,2 , 0)
        self.grid.addWidget(self.thread_edit, 2, 1)

        self.method = QtGui.QLabel('Method')
        self.methodEdit = QtGui.QComboBox(self)
        self.methodEdit.addItem("TCP")
        self.methodEdit.addItem("UDP")
        self.grid.addWidget(self.method, 2, 2)
        self.grid.addWidget(self.methodEdit, 2, 3)

        self.startBtn = QtGui.QPushButton("start",self)
        self.grid.addWidget(self.startBtn, 3, 0, 1, 5)
        self.connect(self.startBtn,QtCore.SIGNAL("clicked()"),self.start)
        self.textBrowser = QtGui.QTextBrowser(self)
        self.grid.addWidget(self.textBrowser, 4, 0, 6, 0)
        self.show()

    def start(self):
        self.host_start_str = str(self.host_start_edit.text())
        self.host_end_str = str(self.host_end_edit.text())
        self.port_start_num = int(self.port_start_edit.text())
        self.port_end_num = int(self.port_end_edit.text())
        self.thread_num = int(self.thread_edit.text())
        self.method_num = self.methodEdit.currentIndex()

        self.daemonthread = DaemonThread(self)
        self.daemonthread.start()
        self.daemonthread.trigger.connect(self.update_text)

    def host_start_change(self, host_start):
        self.host_end_edit.setText(host_start)
    
    def port_start_change(self, port_start):
        self.port_end_edit.setText(port_start)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space:
            self.close()

    def update_text(self, text):
        self.textBrowser.append(text)

def scan(daemon, host, port):
    s = socket.socket()
    protocolname = 'tcp'
    s.settimeout(0.1)
    if s.connect_ex((host, port)) == 0:  
        try:
            print "%4d open => tcp service name: %s" %(port,socket.getservbyport(port,protocolname))
            daemon.trigger.emit("%4d open => tcp service name: %s" %(port,socket.getservbyport(port,protocolname)))
        except:
            print port, 'open => tcp service name: No Found'
            daemon.trigger.emit('%4d open => tcp service name: No Found'%port)
    else:
        pass
    s.close()

def udp_scan(daemon, host, port):
    udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsock.settimeout(0.6)
    freq = 0
    for j in xrange(3):
        udpsock.sendto("", (host, port))
        try:
            data, addr = udpsock.recvfrom(1024)
        except socket.timeout:
            freq += 1
        except Exception,e:
            if e.errno == 10054:
                pass
            else:
                print e,e.errno
    if freq == 3:
        try:
            print "%4d open => udp service name: %s"%(port, socket.getservbyport(port, 'udp'))
            daemon.trigger.emit("%4d open => udp service name: %s" %(port,socket.getservbyport(port,'udp')))
        except:
            print "%4d open => udp service name: %s"%(port, "No Found")
            daemon.trigger.emit("%4d open => udp service name: %s"%(port, "No Found"))
    udpsock.close()

def writeQ(queue, start, end):
    for i in range(start, end+1):
        queue.put(i)

def readQ(queue, daemon, host, start, end, thread):
    for i in range((end-start)/thread + 1):
        try:
            num = queue.get(block=False)
            if daemon.parent.method_num == 0:
                scan(daemon, host, num)
            else:
                udp_scan(daemon, host, num)
        except:
            pass

class DaemonThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        super(DaemonThread, self).__init__(parent)
        self.parent = parent

    def run(self):
        try:
            start_num = ip2num(self.parent.host_start_str)
            end_num = ip2num(self.parent.host_end_str)
        except Exception,e:
            self.trigger.emit("Your Host Input Is wrong ." + str(e) + '\n')
            return 
        self.trigger.emit("Start Scan ... \n")
        for host in xrange(start_num, end_num + 1):
            host = num2ip(host)
            print "---------- "+host+" ---------- \n"
            self.trigger.emit("---------- "+host+" ---------- \n")
            self.thread_scan(host)
        self.trigger.emit("\nEnd Scan .\n")

    def thread_scan(self, host):
        funcs = [writeQ, readQ]
        q = Queue(65535)
        threads = []
        t = threading.Thread(target=funcs[0],args=(q, self.parent.port_start_num, self.parent.port_end_num))
        threads.append(t)
        for i in range(self.parent.thread_num):
            t = threading.Thread(target=funcs[1],args=(q, self, host, self.parent.port_start_num, self.parent.port_end_num, self.parent.thread_num))
            threads.append(t)
        for i in range(self.parent.thread_num + 1):
            threads[i].start()
        for i in range(self.parent.thread_num + 1):
            threads[i].join()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    game = GScan()
    app.exec_()