import os
import sys
import platform


def main():
    if len(sys.argv) != 3:
        print '[!] Usage ', __file__, ' <username> <password>'
        return
    sys.argv = sys.argv[1:]

    username = sys.argv[0]
    password = sys.argv[1]

    system = platform.system()
    if 'Windows' == system:
        from win32com.shell import shell
        if not shell.IsUserAnAdmin():
            print '[!] Need administrator privilege.'
            return

        import win32net
        import win32netcon

        group = 'Administrators'
        user_info = {
            'name': username,
            'password': password,
            'priv': win32netcon.USER_PRIV_USER,
            'home_dir': None,
            'comment': None,
            'flag': win32netcon.UF_SCRIPT,
            'script_path': None,
        }
        user_group_info = {
            'domainandname': username,
        }

        try:
            win32net.NetUserAdd(None, 1, user_info)
            win32net.NetLocalGroupAddMembers(None, group, 3, [user_group_info])
        except Exception as e:
            print e[2].decode('big5')
            pass
    elif 'Linux' == system:
        if os.getuid() != 0:
            print '[!] Need to be root user.'
            return

        os.system('/usr/sbin/useradd -p %s -m -d /home/%s -s /bin/bash %s' % (password, username, username))


main()