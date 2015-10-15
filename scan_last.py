import argparse
import socket  
import sys

def scan(host,port,show):  
	s = socket.socket()  
	s.settimeout(0.1)
	if s.connect_ex((host, port)) == 0:  
		print port, 'open'  
	else:
		if show:
			print port ,'Close'
	s.close()  
if __name__ == '__main__':  
	parser = argparse.ArgumentParser(description="input your host and port")
	parser.add_argument("-o","--on",help="show close",action="store_true")
	parser.add_argument("--host",help="chose host",action="store",default='127.0.0.1',dest="host")
	parser.add_argument("--start",help="chose port start",action="store",type=int,default=0,dest="start")
	parser.add_argument("--end",help="chose port end",action="store",type=int,default=512,dest="end")
	args = parser.parse_args()
	host = args.host
	start = args.start
	end   = args.end
	show = args.on
	for item in range(start,end):
		scan(host,item,show)