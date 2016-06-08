import os
import sys
from Crypto.Cipher import AES

block_size = 16


def pad(s):
    return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)


def unpad(s):
    return s[:-ord(s[len(s)-1])]


def main():
    if len(sys.argv) != 2:
        print '[!] Usage: ', __file__, ' <message>'
        return

    key = os.urandom(32)

    enc = AES.new(key, AES.MODE_ECB)
    enc_msg = enc.encrypt(pad(sys.argv[1]))
    print '[+] Encrypted: ', enc_msg

    dec = AES.new(key, AES.MODE_ECB)
    dec_msg = dec.decrypt(enc_msg)
    print '[+] Decrypted: ', unpad(dec_msg)


main()
