#python端口扫描
===

---
[TOC]

##原理
端口扫描可以用socket尝试连接相应的端口，能连接上即该端口开放着。
需要注意的一点是，因为有的端口关闭的时候，连接时会等待很长时间，所以可以设置timeout，连接超时的时间，如果超过了一定的时间即自动放弃，认为该端口关闭。

##版本
**Version 0.1**
```python
import socket  
def scan(port):  
    s = socket.socket()
    s.settimeout(0.1)  
    if s.connect_ex(('localhost', port)) == 0:  
        print port, 'open'  
    s.close()  
if __name__ == '__main__':  
    map(scan,range(1,65536)) 
```

**Version 0.2**
- 加入了自定义扫描的IP
- 加入了自定义的起始与结束端口

```python
import socket  
import sys

def scan(port):  
    s = socket.socket()  
    s.settimeout(0.1)
    if s.connect_ex((sys.argv[1], port)) == 0:  
        print port, 'open'  
    s.close()  
if __name__ == '__main__':  
	start = int(sys.argv[2])
	end   = int(sys.argv[3])
	map(scan,range(start,end))  
```

**Version 0.3**
- 设置了默认的扫描IP：127.0.0.1
- 设置了默认的扫描端口：0 - 512
- 当然，还是能够自定义扫描IP和端口
- 让端口关闭的也打印出来

```python
import argparse
import socket  
import sys

def scan(host,port):  
	s = socket.socket()  
	s.settimeout(0.1)
	if s.connect_ex((host, port)) == 0:  
		print port, 'open'  
	else:
		print port ,'Close'
	s.close()  
	
if __name__ == '__main__':  
	parser = argparse.ArgumentParser(description="input your host and port")
	parser.add_argument("--host",help="chose host",action="store",default='127.0.0.1',dest="host")
	parser.add_argument("--start",help="chose port start",action="store",type=int,default=0,dest="start")
	parser.add_argument("--end",help="chose port end",action="store",type=int,default=512,dest="end")
	args = parser.parse_args()
	host = args.host
	start = args.start
	end   = args.end
	for item in range(start,end):
		scan(host,item)
```

**Version 1.0**
- 参数1 ： '-o' 或者 '--on' 选择是否显示关闭的端口，默认关闭
- 参数2 ： '--host=' 选择将要扫描的IP，默认为127.0.0.1
- 参数3 ： '--start=' 选择将要扫描的IP开始端口，默认为0
- 参数4 ： '--end=' 选择将要扫描的IP结束端口，默认为512