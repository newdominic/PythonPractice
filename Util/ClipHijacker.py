import pyperclip
import time

clips = []

while True:
    if pyperclip.paste() != 'None':
        clip = pyperclip.paste()

        if clip not in clips:
            clips.append(clip)
            print clips

        time.sleep(2)
