# suppress scapy warning
# http://stackoverflow.com/a/13249436/3925588
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

PORT = 80

conf.iface = "en0"
conf.verb = 0


for i in range(1, 254):
    host = "192.168.0.%d" % i
    ret = sr1(IP(dst=host)/TCP(dport=PORT, flags="S"), timeout=0.2, verbose=0)
    if ret is not None:
        print "[*] host:", host, "has port %d on." % PORT
    else:
        print "[!] host:", host, "port %d down." % PORT


print "[!] SYN scan done."