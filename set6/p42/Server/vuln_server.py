from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import *
from secret import flag

HASH_ASN1 = {  
    '\x30\x20\x30\x0c\x06\x08\x2a\x86\x48\x86\xf7\x0d\x02\x05\x05\x00\x04\x10'.encode("hex").decode("hex"): 'MD5',
    '\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14'.encode("hex").decode("hex"): 'SHA-1',
    '\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20'.encode("hex").decode("hex"): 'SHA-256',
    '\x30\x41\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x02\x05\x00\x04\x30'.encode("hex").decode("hex"): 'SHA-384',
    '\x30\x51\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x03\x05\x00\x04\x40'.encode("hex").decode("hex"): 'SHA-512',
}

publickey = RSA.importKey(open("public.key",'r').read())
n = publickey.n
e = publickey.e

def _find_method_hash(s):
	for i in HASH_ASN1:
		if s.startswith(i):
			return (HASH_ASN1[i], s[len(i):])
	raise VerificationError('Signature Verification Failed!')

def _get_hash(algo, s):
	if algo == "MD5":
		h = MD5.new()
		h.update(s)
		return h.digest()
	elif algo == "SHA-1":
		h = SHA.new()
		h.update(s)
		return h.digest()
	elif algo == "SHA-256":
		h = SHA256.new()
		h.update(s)
		return h.digest()
	elif algo == "SHA-384":
		h = SHA384.new()
		h.update(s)
		return h.digest()
	elif algo == "SHA-512":
		h = SHA512.new()
		h.update(s)
		return h.digest()


def _verify(message, signature):
	signature = int(signature, 16)
	asn1_data = long_to_bytes(pow(signature, e, n))

	if asn1_data[0] != "\x00":
		asn1_data = "\x00" + asn1_data
	
	if asn1_data[:2] != "\x00\x01":
		raise VerificationError("Signature Verification Failed!")
		#print "Koi baat nahi"
	else:
		asn1_data = asn1_data[2:]
		index = asn1_data.find('\x00')
		
		if index == -1:
			raise VerificationError("Signature Verification Failed!")
		
		asn1_data = asn1_data[index+1:]
		hash_algo, hash_str = _find_method_hash(asn1_data)
		print hash_algo, hash_str.encode("hex")

		hash_message = _get_hash(hash_algo, message)
		if hash_message != hash_str:
			raise VerificationError("Signature Verification Failed!")
	print "Wow, you just got the correct signature, I think I am gonna give you the flag now: ", flag

# Signature obtained from the exploit script ../exploit.py
signature = "012173244cfbd857eea633edfa750d23c8977594804a998c2de1e8022e33759dd71327e3564d0dc5d1a961"
_verify("challenge", signature)