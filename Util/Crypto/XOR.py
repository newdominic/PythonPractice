import sys
import string
import random


key_size = 1024
xor_key = ''.join(random.choice(string.letters + string.digits + string.punctuation) for _ in range(key_size))


def str_xor(input_string, key):
    return ''.join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(input_string, key)])


def main():
    if len(sys.argv) != 2:
        print '[!] Usage: ', __file__, ' <string>.'
        return

    input_string = sys.argv[1]
    print '[*] Input string: ', input_string

    enc = str_xor(input_string, xor_key)
    print '[+] Encrypted string: ', enc

    dec = str_xor(enc, xor_key)
    print '[+] Decrypted string: ', dec

main()
