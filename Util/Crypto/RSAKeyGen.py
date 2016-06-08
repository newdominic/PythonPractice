from Crypto.PublicKey import RSA

new_key = RSA.generate(4096)

public_key = new_key.publickey().exportKey('PEM')
print public_key
with open('public.pem', 'w') as f:
    f.write(public_key)


private_key = new_key.exportKey('PEM')
print private_key
with open('private.pem', 'w') as f:
    f.write(private_key)
