import os
import sys
import base64
import platform
import tempfile
import subprocess


def b64e(x):
    return base64.b64encode(x)


def normalize_path_args(args):
    single_quote_token = b64e('SGQT')
    double_quote_token = b64e('DBQT')
    space_token = b64e('SPCT')
    backslash_token = b64e('BKST')
    args = args.replace('\\\'', single_quote_token)
    args = args.replace('\\"', double_quote_token)
    args = args.replace('\\ ', space_token)
    args = args.replace('\\\\', backslash_token)

    args = args.replace('\'', '"')

    index = 0
    arg_list = []
    prev_quote_ret2 = 0
    while index < len(args):
        quote_ret = args.find('"', index)
        space_ret = args.find(' ', index)
        if quote_ret == -1 and space_ret == -1:
            break
        elif quote_ret != -1 and (space_ret == -1 or space_ret != -1 and quote_ret < space_ret):
            quote_ret2 = args.find('"', quote_ret+1)
            if quote_ret2 == -1:
                print "[!] Error: Quote matching failed in normalize_path_args()."
                return []

            arg = args[quote_ret+1: quote_ret2]
            arg = arg.replace (' ', space_token)

            # concat string
            if quote_ret == prev_quote_ret2 + 1:
                arg_list[-1] = arg_list[-1] + arg
            else:
                arg_list.append(arg)

            index = quote_ret2 + 1
            prev_quote_ret2 = quote_ret2
        else:
            arg_list.append(args[index:space_ret])

            index = space_ret+1

    arg_list.extend(args[index:].split(' '))
    if '' in arg_list:
        arg_list = [ x for x in arg_list if x != '']

    for i in range(0, len(arg_list)):
        arg_list[i] = arg_list[i].replace(single_quote_token, '\\\'')
        arg_list[i] = arg_list[i].replace(double_quote_token, '\\"')
        arg_list[i] = arg_list[i].replace(space_token, '\\ ')
        arg_list[i] = arg_list[i].replace(backslash_token, '\\\\')

    return arg_list


def linux_search_file(arg_list):
    if len(arg_list) == 1:
        dir_path = '/'
    else:
        dir_path = arg_list[1]

    if not os.path.isdir(dir_path):
        print '[!] %s is not a directory' % dir_path
        return

    cmd = subprocess.Popen('find %s -name \'%s\'' % (dir_path, arg_list[0]), shell=True, stdout=subprocess.PIPE)
    print cmd.stdout.read()


def windows_search_file(arg_list):
    if len(arg_list) == 1:
        import win32api
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        for drive in drives:
            command = 'dir %s%s /S' % (drive, arg_list[0])
            print command
            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            print cmd.stdout.read()

    else:
        dir_path = arg_list[1]
        if not os.path.isdir(dir_path):
            print '[!] %s is not a directory' % dir_path
            return

        # find path format
        temp_path_1 = tempfile.mkdtemp()
        temp_process = subprocess.Popen('dir %s' % temp_path_1, shell=True, stdout=subprocess.PIPE)
        result = temp_process.stdout.read().split('\r\n')
        tag_position = -1
        for line in result:
            if ':\\' in line:
                tag_position = -(len(line.replace(temp_path_1, '').split(' ')) - 2)
                break

        if dir_path[-2] == ':' and dir_path[-1] == '\\':
            dir_path = dir_path[0:-1]

        cmd = subprocess.Popen('dir %s\%s /S' % (dir_path, arg_list[0]), shell=True, stdout=subprocess.PIPE)
        result = cmd.stdout.read()
        result = result.split('\r\n')
        cur_path = ''
        for line in result:
            if ':\\' in line:
                cur_path = ' '.join(line.split(' ')[1:tag_position])
            else:
                import datetime
                line_split = line.split(' ')
                try:
                    # YY/MM/DD AMorPM Time SIZE file
                    datetime.datetime.strptime(line_split[0], '%Y/%m/%d')
                    line_split = [x for x in line_split if x != '']
                    file_name = ' '.join(line_split[4:])
                    print '%s\%s' % (cur_path, file_name)
                except:
                    pass


def main():
    sys.argv = sys.argv[1:]
    args = ' '.join(sys.argv)
    arg_list = normalize_path_args(args)
    arg_num = len(arg_list)
    if arg_num == 0 or arg_num > 2:
        print '[!] Usage: %s <filename> [<directory>]' % __file__
        return

    system = platform.system()
    if 'Linux' == system:
        linux_search_file(arg_list)
    elif 'Windows' == system:
        windows_search_file(arg_list)
    else:
        pass

main()
