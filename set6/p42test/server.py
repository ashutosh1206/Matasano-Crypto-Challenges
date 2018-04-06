from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from Crypto.Hash import *
from Crypto.Signature import PKCS1_v1_5

p = getPrime(512)
e = 65537
q = getPrime(512)
n = p*q
phin = (p-1)*(q-1)
d = inverse(e, phin)
print "n : ", n
print "e : ", e

key = RSA.construct((long(n), long(e), long(d)))
key2 = RSA.construct((long(n), long(e)))
f = open("public.key",'w')
f.write(key2.exportKey('PEM'))

assert key.n == n
assert key.e == e

# -------------------Signing the message------------------------
message = "Test message being signed"
h = SHA.new(message)
signer = PKCS1_v1_5.new(key)

signature = signer.sign(h)
print signature.encode("hex")

# ---------------------Signature verification-------------------
verifier = PKCS1_v1_5.new(key2)
print verifier.verify(h, signature)
if verifier.verify(h, signature):
	print "Correct"
else:
	print "Incorrect"
# -----------------End of library documentation testing---------