#coding=utf-8

import threading
from Queue import Queue
from time import ctime
import socket  
import sys

def scan(port):  
	s = socket.socket()  
	s.settimeout(0.1)
	if s.connect_ex((sys.argv[1], port)) == 0:  
		print port, 'open'  
	s.close()  

def writeQ(queue,start,end):
	for i in range(start,end):
		queue.put(i,1)

def readQ(queue,start,end):
	for i in range((end-start)/2):
		num = queue.get(1)
		scan(num)

print "all start at: ",ctime()

start = int(sys.argv[2])
end   = int(sys.argv[3])

funcs = [writeQ,readQ]
nfunc = range(len(funcs))

q = Queue(65535)
threads = []

t = threading.Thread(target=funcs[0],args=(q,start,end))
threads.append(t)	

for i in range(2):
	t = threading.Thread(target=funcs[1],args=(q,start,end))
	threads.append(t)	

for i in range(3):
	threads[i].start()

for i in range(3):
	threads[i].join()

print "all end   at: ",ctime()	