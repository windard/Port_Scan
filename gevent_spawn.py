# coding=utf-8

from gevent import monkey


monkey.patch_all()

import gevent
import socket


def scan(host, port, show):
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
    threads = [gevent.spawn(scan, *(host, port, False))
               for port in xrange(start, end)]
    gevent.joinall(threads)


if __name__ == '__main__':
    scan_all(0, 10000, '127.0.0.1')
