#!/usr/bin/env python2
import sys
import ecdh
import hmac
from Crypto.Util.number import *
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

assert isPrime(233970423115425145524320034830162017933)
p = 233970423115425145524320034830162017933
a = -95051 % p
b = 11279326

E = ecdh.CurveFp(p, a, b)
P = ecdh.Point(E, 182, 85518893674295321206118380980485522083, 29246302889428143187362802287225875743)
print "Welcome to Diffie Hellman Key Exchange!"
print "Here, take my public key: ", x*P

_Qx = int(raw_input("Give me the x-coordinate of your public key: "))
_Qy = int(raw_input("Give me the y-coordinate of your public key: "))
Q = ecdh.Point(E, _Qx, _Qy)

message = "test"
print "Here is the message: ", message
shared_secret = x * Q
# print shared_secret.x()
print "Here is the corresponding hmac: ", hmac.new(long_to_bytes(shared_secret.x()), message).hexdigest()
