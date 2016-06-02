import sys
import socket

RECV_BYTE = 1024    

def connect():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind ((sys.argv[0], int(sys.argv[1])))
    s.listen(1)
    print '[*] Waiting for connection...'
    conn, addr = s.accept()
    print '[+] Accept connection from ', addr

    while True:

        command = raw_input("#> ")

        if 'exit' in command or 'quit' in command:
            conn.send('exit')
            conn.close()
            break
        else:
            conn.send(command)
            print conn.recv(RECV_BYTE)


def main():
    if len(sys.argv) < 3:
        print '[!] Usage: Basic_Server.py <host> <port>'
        return

    sys.argv = sys.argv[1:]
    connect()


main()
