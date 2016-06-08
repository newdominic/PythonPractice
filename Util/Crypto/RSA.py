import sys
from Crypto.PublicKey import RSA


def main():
    if len(sys.argv) < 2:
        print '[!] Usage: ', __file__, ' <message>'
        return

    public_key = open('public.pem', 'r')
    enc = RSA.importKey(public_key)
    enc_msg = enc.encrypt(' '.join(sys.argv[1:]), 0)
    print '[+] Encrypted: ', enc_msg

    private_key = open('private.pem', 'r')
    dec = RSA.importKey(private_key)
    dec_msg = dec.decrypt(enc_msg)
    print '[+] Decrypted: ', dec_msg

main()
