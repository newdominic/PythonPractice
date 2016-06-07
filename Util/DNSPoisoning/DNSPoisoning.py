import subprocess
import sys
import os


def main():
    if len(sys.argv) != 3:
        print '[!] Usage: ', __file__, ' <ip_address> <hostname>.'
        return
    sys.argv = sys.argv[1:]

    if os.name == 'nt':
        from win32com.shell import shell
        
        if not shell.IsUserAnAdmin():
            print '[!] Current user has no privilege.'
            return

        poisoning_cmd = '\necho %s %s >> C:\Windows\System32\drivers\etc\hosts\n' % (sys.argv[0], sys.argv[1])
        subprocess.Popen(poisoning_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        subprocess.Popen('ipconfig /flushdns', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif os.name == 'posix':
        if os.getuid() != 0:
            print '[!] Current user has no privilege.'
            return

        poisoning_cmd = '\necho %s %s >> /etc/hosts\n' % (sys.argv[0], sys.argv[1])
        subprocess.Popen(poisoning_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

main()
