import socket, sys

ARGV_NUM = 3
ARGV = "host port"
USAGE = "Usage: python " + __file__ + " " + ARGV


def usage():
    print USAGE


def run(target_host, target_port):
    # create socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    client.connect((target_host, target_port))

    # interact with server, send SIGINT to stop the program

    print "#:",
    msg = raw_input()
    client.send(msg)

    response = client.recv(2048)

    print response

    client.close ()

if __name__ == "__main__":
    if len(sys.argv) < ARGV_NUM:
        usage()
        exit()

    run(sys.argv[1], int(sys.argv[2]))