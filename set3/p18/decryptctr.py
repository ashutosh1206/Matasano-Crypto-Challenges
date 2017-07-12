from Crypto.Cipher import AES
import struct

key = "YELLOW SUBMARINE"


class secret:
    def __init__(self, nonce, cnt):
        self.nonce = nonce
        self.cnt = cnt

    def count(self):
        c1 = struct.pack("<Q", self.nonce)
        c2 = struct.pack("<Q", self.cnt)
        self.cnt += 1
        c3 = c1 + c2
        print c3
        return c3

ciphertext = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
ciphertext = ciphertext.decode("base64")
nonce = 0
cnt = 0
obj = secret(nonce,cnt)
cipher = AES.new(key, AES.MODE_CTR, counter=obj.count)
print cipher.decrypt(ciphertext)

    