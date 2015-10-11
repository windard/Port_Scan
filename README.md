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
- 加入了自定义扫描的URL
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
