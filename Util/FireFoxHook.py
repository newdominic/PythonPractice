from winappdbg import Debug, EventHandler
import sys

search_str = ''
debug = None
process = None


def PR_Write(event, ra, arg1, arg2, arg3):
    global debug
    global process
    global search_str

    data = process.read(arg2, 1024)
    if search_str in data:
        print data
        print '[+] ', search_str, ' found.'
        debug.stop()
        print '[*] FireFoxHook stopped.'


class MyEventHandler(EventHandler):

    def load_dll(self, event):
        module = event.get_module()
        if module.match_name('nss3.dll'):
            pid = event.get_pid()
            address = module.resolve('PR_Write')
            print '[+] Found PR_Write at 0x%x' % address
            event.debug.hook_function(pid, address, preCB=PR_Write, postCB=None, paramCount=3, signature=None)


def main():
    global debug
    global process
    global search_str

    if len(sys.argv) != 2:
        print '[!] Usage: ', __file__, ' <search_string>'
        return

    search_str = sys.argv[1]

    debug = Debug(MyEventHandler())

    try:
        for (process, name) in debug.system.find_processes_by_filename('firefox.exe'):
            pid = process.get_pid()
            print '[+] Found %s with PID %s' % (name, pid)

        if process is not None:
            debug.attach(pid)
            print '[+] Attaching PID %s...' % pid
            debug.loop()
        else:
            print '[!] firefox.exe not found.'
    except Exception as e:
        debug.stop()
        print '[*] FireFoxHook stopped.'

main()

