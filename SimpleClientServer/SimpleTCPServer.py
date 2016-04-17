import socket, sys

ARGV_NUM = 2
ARGV = "port"
USAGE = "Usage: python " + __file__ + " " + ARGV


def usage():
    print USAGE


def run(port):
    bind_ip = "0.0.0.0"
    bind_port = port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((bind_ip, bind_port))
    
    server.listen(1)

    print "[*] Listening on %s %d" % (bind_ip, bind_port)

    # waiting for connection
    client, addr = server.accept()
    
    print "[*] Accepted connection from: %s %d" % (addr[0], addr[1])

    while True:
        request = client.recv(2048)
        
        print "[*] Received message: %s" % request

        client.send("ECHO: %s" % request)

if __name__ == "__main__":
    if len(sys.argv) < ARGV_NUM:
        usage()
        exit()

    run(int(sys.argv[1]))
