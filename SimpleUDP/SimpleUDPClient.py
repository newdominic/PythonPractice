import socket, sys

ARGV_NUM = 3
ARGV = "host port"
USAGE = "Usage: python " + __file__ + " " + ARGV


def usage():
    print USAGE


def run(target_host, target_port):
    addr = (target_host, target_port)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print "#:",
    msg = raw_input ()
    client.sendto (msg, addr)

    response, serv_addr = client.recvfrom (1024)

    print response


if __name__ == "__main__":
    if len(sys.argv) < ARGV_NUM:
        usage()
        exit()

    run(sys.argv[1], int(sys.argv[2]))