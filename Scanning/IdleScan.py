# https://nmap.org/book/idlescan.html

import sys, socket
from scapy.all import *

conf.verb = 0


def idle_scan(idle_host, target_host, target_port):

    # first SYN/ACK to retrieve initial id
    print "[*] Sending first request..."
    first_response = sr1(IP(dst=idle_host)/TCP(sport=5566, dport=4321, flags="SA"), timeout=5)
    if first_response is None:
        print "[!] First request FAILED."
        return

    first_response_id = first_response.id

    print "[*] Idle host INIT RST ID: %d" % first_response_id

    # send SYN to target host with src ip of idle host
    print "[*] Sending second request..."
    sr1(IP(dst=target_host, src=idle_host)/TCP(sport=5566, dport=target_port, flags="S"), timeout=5)

    # second SYN/ACK to retrieve final id
    print "[*] Sending final request..."
    final_response = sr1(IP(dst=idle_host)/TCP(sport=5566, dport=4321, flags="SA"), timeout=5)
    if final_response is None:
        print "[!] Final request FAILED."
        return
    
    final_response_id = final_response.id

    print "[*] Idle host FINAL RST ID: %d" % final_response_id

    if final_response_id - first_response_id > 2:
        print "[+] Host: %s Port: %d opened" % (target_host, target_port)
    else:
        print "[-] Host: %s Port: %d closed" % (target_host, target_port)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "[!] Usage: python", __file__, "<idle_host> <target_host> <target_port>"
        sys.exit(0)

    idle_host = sys.argv[1]
    try:
        socket.inet_aton(idle_host)
    except socket.error:
        print "[!] <idle_host> missing."
        sys.exit(0)

    target_host = sys.argv[2]
    try:
        socket.inet_aton(target_host)
    except socket.error:
        print "[!] <target_host> missing."
        sys.exit(0)

    try:
        target_port = int(sys.argv[3])
    except ValueError:
        print "[!] <target_port> missing."
        sys.exit(0)

    idle_scan(idle_host, target_host, target_port)
