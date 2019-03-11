from Crypto.Util.number import *
import random

def euler_criterion(a, p):
    assert GCD(a, p) == 1
    if pow(a, (p - 1) / 2, p) == 1:
        return 1
    if pow(a, (p - 1) / 2, p) == p - 1:
        return 0
    return
    return


def factorize_get_Q_S(num):
    Q = num
    S = 0
    while Q % 2 == 0:
        Q = Q / 2
        S += 1

    assert Q * 2 ** S == num
    return (
     Q, S)


def tonelli_shanks(n, p):
    assert isPrime(p)
    try:
        assert euler_criterion(n, p) == 1
    except:
        print "Euler's Criterion is not satisfied, `n` is not a quadratic residue"
        return -1

    Q, S = factorize_get_Q_S(p - 1)
    for i in range(2, p - 1):
        potential_z = i
        if euler_criterion(potential_z, p) == 0:
            z = potential_z
            break

    M = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    R = pow(n, (Q + 1) / 2, p)
    while True:
        if t == 0:
            return 0
        if t == 1:
            assert pow(R, 2, p) == n
            return (
             R, -R % p)
        res = t
        save_i = -1
        for i in range(1, M):
            res = res ** 2 % p
            if res == 1:
                save_i = i
                break

        assert save_i != -1
        i = save_i
        b = pow(c, pow(2, M - i - 1, p - 1), p)
        M = i
        c = pow(b, 2, p)
        t = t * b ** 2 % p
        R = R * b % p


if __name__ == '__main__':
    print tonelli_shanks(5, 41)
    print tonelli_shanks(10, 13)
    for i in [2, 5, 6, 7, 8, 11]:
        print tonelli_shanks(2, 13)
    
