from Crypto.Cipher import AES
import struct

key = "YELLOW SUBMARINE"
nonce = 0
cnt = 0

class secret:
    def count(nonce, cnt):
        c1 = struct.pack("<Q", nonce)
        c2 = struct.pack("<Q", cnt)
        cnt += 1
        c3 = c1 + c2
        print c3
        return c3

ciphertext = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="

cipher = AES.new(key, AES.MODE_CTR, counter=secret.count(nonce, cnt))
print cipher.decrypt(ciphertext)

