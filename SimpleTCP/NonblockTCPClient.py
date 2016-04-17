import socket, sys, threading

ARGV_NUM = 3
ARGV = "host port"
USAGE = "Usage: python " + __file__ + " " + ARGV


def usage():
    print USAGE


def client_recv_handler(server):
    while True:
        try:
            response = server.recv(2048)

            print response
        except socket.timeout:
            pass


def client_send_handler(server):
    while True:
        buffer = raw_input()

        server.send(buffer)


def run(target_host, target_port):
    # create socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    client.connect((target_host, target_port))

    client_recv_thread = threading.Thread(target=client_recv_handler, args=(client,))
    client_recv_thread.start()

    client_send_thread = threading.Thread(target=client_send_handler, args=(client,))
    client_send_thread.start()


if __name__ == "__main__":
    if len(sys.argv) < ARGV_NUM:
        usage()
        exit()

    run(sys.argv[1], int(sys.argv[2]))