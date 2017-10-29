# coding=utf-8

import socket
from Queue import Queue
from concurrent.futures import ThreadPoolExecutor


def scan(args):
    host, port, show = args
    s = socket.socket()
    protocolname = 'tcp'
    s.settimeout(0.1)
    try:
        if s.connect_ex((host, port)) == 0:
            try:
                print "%4d open => service name: %s" % (
                    port, socket.getservbyport(port, protocolname))
            except:
                print '%4d open => service name: No Found' % port
        elif show:
                print port, 'Close'
    except TypeError:
        pass
    s.close()


def scan_all(start, end, host):
    q = Queue(500)
    map(q.put, [(host, port, False) for port in xrange(start, end)])
    with ThreadPoolExecutor(max_workers=500) as executor:
        for i in range(500):
            executor.submit(scan, q)


if __name__ == '__main__':
    scan_all(0, 10000, '127.0.0.1')
