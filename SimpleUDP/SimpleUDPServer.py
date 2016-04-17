import socket, sys

ARGV_NUM = 2
ARGV = "port"
USAGE = "Usage: python " + __file__ + " " + ARGV


def usage():
    print USAGE


def run(bind_port):
    bind_ip = '127.0.0.1'

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server.bind ((bind_ip, bind_port))
    print "[*] Listening on %s %d" % (bind_ip, bind_port)

    while True:
        request, addr = server.recvfrom(1024)

        print "[*] Received message from %s %d: %s" % (addr[0], addr[1], request)

        echo_msg = "ECHO: %s" % request
        print echo_msg
        server.sendto (echo_msg, addr)


if __name__ == "__main__":
    if len(sys.argv) < ARGV_NUM:
        usage()
        exit()

    run(int(sys.argv[1]))