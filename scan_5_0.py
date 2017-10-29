# -*- coding: utf-8 -*-

import socket
import argparse
import multiprocessing


ip2num = lambda x: sum(
    [256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
num2ip = lambda x: '.'.join(
    [str(x / (256 ** i) % 256) for i in range(3, -1, -1)])


def scan(host, port, show):
    s = socket.socket()
    protocolname = 'tcp'
    s.settimeout(0.1)
    if s.connect_ex((host, port)) == 0:
        try:
            print "%s:%4d open => service name: %s" % (
                host, port, socket.getservbyport(port, protocolname))
        except:
            print '%s:%4d open => service name: No Found' % (host, port)
    elif show:
        print port, 'Close'
    s.close()


def udp_scan(host, port, show):
    udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    protocolname = 'udp'
    udpsock.settimeout(0.6)
    freq = 0
    for j in xrange(3):
        udpsock.sendto("", (host, port))
        try:
            data, addr = udpsock.recvfrom(1024)
        except socket.timeout:
            freq += 1
        except Exception, e:
            if e.errno == 10054:
                pass
            else:
                print tuple(e)
    if freq == 3:
        try:
            print "%s:%4d open => udp service name: %s" % (
                host, port, socket.getservbyport(port, protocolname))
        except:
            print "%s:%4d open => udp service name: %s" % (
                host, port, "No Found")
    elif show:
        print port, 'Close'
    udpsock.close()


def writeQ(queue, host_start, host_end, port_start, port_end):
    for host in xrange(ip2num(host_start), ip2num(host_end)):
        for port in xrange(port_start, port_end):
            queue.put((num2ip(host), port))


def readQ(queue, show, udp):
    while not queue.empty():
        try:
            host, port = queue.get()
            if udp:
                udp_scan(host, port, show)
            else:
                scan(host, port, show)
        finally:
            queue.task_done()


def port_scan(host, host_start, host_end, port, port_start, port_end,
              thread_num, show, udp):
    q = multiprocessing.JoinableQueue(500)
    if port != 0:
        multiprocessing.Process(target=writeQ, args=(
        q, host_start, host_end, port, port + 1)).start()
    else:
        multiprocessing.Process(target=writeQ, args=(
        q, host_start, host_end, port_start, port_end)).start()

    for thread in xrange(thread_num):
        multiprocessing.Process(target=readQ, args=(q, show, udp)).start()
    q.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="input your host and port")
    parser.add_argument("-o", "--on", help="show close", action="store_true")
    parser.add_argument("-u", "--udp", help="UDP scan", action="store_true")
    parser.add_argument("--host", help="chose host", action="store",
                        default='127.0.0.1', dest="host")
    parser.add_argument("--host_start", help="chose host_start",
                        action="store", default='127.0.0.1', dest="host_start")
    parser.add_argument("--host_end", help="chose host_end", action="store",
                        default='127.0.0.2', dest="host_end")
    parser.add_argument("--port", help="chose port", action="store",
                        default=0, type=int, dest="port")
    parser.add_argument("--port_start", help="chose port port_start",
                        action="store", type=int, default=0, dest="port_start")
    parser.add_argument("--port_end", help="chose port port_end",
                        action="store", type=int, default=512, dest="port_end")
    parser.add_argument("--thread", help="how much thread", action="store",
                        type=int, default=4, dest="thread")
    args = parser.parse_args()
    host = args.host
    host_start = args.host_start
    host_end = args.host_end
    port = args.port
    port_start = args.port_start
    port_end = args.port_end
    thread_num = args.thread
    show = args.on
    udp = args.udp
    port_scan(host, host_start, host_end, port, port_start, port_end,
              thread_num, show, udp)
