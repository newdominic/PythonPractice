import os
import sys
from Crypto.Cipher import AES


def main():
    if len(sys.argv) != 2:
        print '[!] Usage: ', __file__, '<message>'
        return

    counter = os.urandom(16)
    key = os.urandom(32)

    enc = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    enc_msg = enc.encrypt(sys.argv[1])
    print '[+] Encrypted: ', enc_msg

    dec = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    dec_msg = dec.decrypt(enc_msg)
    print '[+] Decrypted: ', dec_msg

main()
