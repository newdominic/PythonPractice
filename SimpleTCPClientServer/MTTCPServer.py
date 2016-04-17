import socket, sys, threading

ARGV_NUM = 2
ARGV = "port"
USAGE = "Usage: python " + __file__ + " " + ARGV


def usage():
    print USAGE


def handle_client(client, addr):
    request = client.recv(2048)

    print "[*] Received message from %s %d: %s" % (addr[0], addr[1], request)

    client.send("ECHO: %s" % request)

    client.close ()


def run(port):
    bind_ip = "0.0.0.0"
    bind_port = port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((bind_ip, bind_port))

    server.listen(5)

    print "[*] Listening on %s %d" % (bind_ip, bind_port)

    while True:
        # waiting for connection
        client, addr = server.accept()

        print "[*] Accepted connection from: %s %d" % (addr[0], addr[1])

        # threading handle
        client_handler = threading.Thread(target=handle_client, args=(client, addr,))
        client_handler.start()


if __name__ == "__main__":
    if len(sys.argv) < ARGV_NUM:
        usage()
        exit()

    run(int(sys.argv[1]))
