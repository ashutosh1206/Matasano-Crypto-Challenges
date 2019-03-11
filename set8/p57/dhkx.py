#!/usr/bin/env python2
from Crypto.Cipher import AES
from Crypto.Util.number import *
import os, sys
import hmac

from secret import x

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

p = 7199773997391911030609999317773941274322764333428698921736339643928346453700085358802973900485592910475480089726140708102474957429903531369589969318716771
g = 4565356397095740655436854503483826832136106141639563487732438195343690437606117828318042418238184896212352329118608100083187535033402010599512641674644143
q = 236234353446506858198510045061214171961
assert pow(g, q, p) == 1

if __name__ == "__main__":
    print "Welcome to DHKX protocol suite"
    print "Here, take my public key: ", pow(g, x, p)
    _h = int(raw_input("Give me your public key: "))
    _shared_secret = pow(_h, x, p)
    _message = "test"
    print "Here is the message: ", _message
    print "Here is the corresponding hmac: ", hmac.new(long_to_bytes(_shared_secret), _message).hexdigest()
