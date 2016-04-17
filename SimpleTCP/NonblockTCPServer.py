import socket, sys, threading

ARGV_NUM = 2
ARGV = "port"
USAGE = "Usage: python " + __file__ + " " + ARGV


def usage():
    print USAGE


def server_recv_handler(client):
    while True:
        try:
            request = client.recv(2048)

            print request
        except:
            pass


def server_send_handler(client):
    while True:
        buffer = raw_input()

        client.send(buffer)


def run(port):
    bind_ip = "0.0.0.0"
    bind_port = port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)

    server.bind((bind_ip, bind_port))
    
    server.listen(1)

    print "[*] Listening on %s %d" % (bind_ip, bind_port)

    # waiting for connection
    while True:
        try:
            client, addr = server.accept()

            print "[*] Accepted connection from: %s %d" % (addr[0], addr[1])

            server_recv_thread = threading.Thread(target=server_recv_handler, args=(client,))
            server_recv_thread.start()

            server_send_thread = threading.Thread(target=server_send_handler, args=(client,))
            server_send_thread.start()
        except:
            pass


if __name__ == "__main__":
    if len(sys.argv) < ARGV_NUM:
        usage()
        exit()

    run(int(sys.argv[1]))
