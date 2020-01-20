#!/usr/bin/env python2.7
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse, GCD
from Crypto.Random import random
from ecc import CurveFp, Point, INFINITY
import hashlib

def slice_string(s, _len):
    """
    Function that slices the string `s` taking `_len` most significant bits
    :parameters:
        s    : str
                String to be sliced
        _len : int/long
                Number of most significant bits to be sliced from s
    """
    return long_to_bytes(int(bin(bytes_to_long(s))[2:2+_len], 2))

hash_dict = {}

# Parameters of Curve P-256
# Taken from https://safecurves.cr.yp.to/
p = 2**256 - 2**224 + 2**192 + 2**96 - 1
a = p-3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
E = CurveFp(p, a, b)
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369

# Generator point for the curve P-256
_Px = 28970321132810407204399320564493926615887394783622447137349951821710009632774
_Py = 5469808291017593166892350402328489948321321599894853070991076161657484313730
P = Point(E, _Px, _Py)

class ECDSA:
    def __init__(self, EC, base_pt, order_base_pt):
        self.E = EC
        self.G = base_pt
        self.n = order_base_pt
        assert self.n * self.G == INFINITY
    
    def sign(self, message, d, hash):
        assert hash.__name__[8:] in list(hashlib.algorithms)
        e = hash(message).digest()
        Ln = len(bin(self.n)[2:].replace("L", ""))
        z = bytes_to_long(slice_string(e, Ln))
        k = random.randint(1, self.n-1)
        r = (k * self.G).x()
        assert GCD(k, self.n) == 1
        s = (inverse(k, self.n)*(z + r*d)) % self.n
        return (r, s)
    
    def verify(self, signature, message, public_key, hash):
        try:
            assert E.contains_point(public_key.x(), public_key.y())
            r, s = signature
            assert GCD(s, self.n) == 1
            assert r >= 1
            assert hash.__name__[8:] in list(hashlib.algorithms)
        except:
            return False
        e = hash(message).digest()
        Ln = len(bin(self.n)[2:].replace("L", ""))
        z = bytes_to_long(slice_string(e, Ln))
        s_inv = inverse(s, self.n)
        u_1 = (s_inv*z) % self.n
        u_2 = (s_inv*r) % self.n
        T = u_1*self.G + u_2*public_key
        return r == T.x()


# Adam signs a message using his private key d_adam
d_adam = 1234
public_key = d_adam*P
D = ECDSA(E, P, n)
r, s = D.sign("ashutosh", d_adam, hashlib.md5)

# Eve's side
e = hashlib.md5("ashutosh").digest()
Ln = len(bin(n)[2:].replace("L", ""))
z = bytes_to_long(slice_string(e, Ln))
s_inv = inverse(s, n)
u_1 = (s_inv*z) % n
u_2 = (s_inv*r) % n
T = u_1*P + u_2*public_key

# Eve's secret key
_d = 123
t = u_1 + u_2*_d
_G = inverse(t, n)*T
_Q = _d*_G
F = ECDSA(E, _G, n)

# Note that (r, s) is verified by Eve's public key
print(F.verify((r, s), "ashutosh", _Q, hashlib.md5))