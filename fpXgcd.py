#!/usr/bin/env python3 -i

from fractions import Fraction as F

print("Try: p,q = 19, (2**32-1) // 17; T = fpSplit(p,q); p,q, sum([F(*t) for t in T]), T")

def DM(a,b): # divmod minimizing absolute value of remainder
    d,m = divmod(a,b)
    return (d+1, m-b) if 2*m > b else (d,m)

def fpSplit(p, q): # Partial Fractions into Fermat Prime Factors
    '''Splits a rational p/q into fermat prime rationals n/1 + a/3 + b/5 + c/17 + d/257 + e/65537'''
    N, D = [-2, 1, 4, 2, 64, 32768], (1, 3, 5, 17, 257, 65537)

    if q == 0:
       print("Error: Divide by 0")
       return None

    if 0xFFffFFff % q != 0:
       print('Error: 0xFFffFFff %% %s = %s != 0 (fermat prime split does not exist)' % (q, 0xFFffFFff % q))
       return None

    n = p * 0xFFffFFff//q
    d, m = divmod(n, 2**32-1)
    dmt  = [ DM(t[0]*m, t[1]) + (t[1],) for t in zip(N, D) ]
    d += sum([dm[0] for dm in dmt ])
    ft = [ (dm[1], dm[2]) for dm in dmt[1:] if dm[1] != 0 ]
    if d != 0: ft = [(d, 1)] + ft

    if 1:
        s = ' + '.join([ 'F(%s, %s)' % (a,b) for a,b in ft ])
        cmd = 'F(%s, %s) == F(%s, 2**32-1) == %s' % (p,q, n, s)
        print('Check (%s): %s' % (eval(cmd), cmd))

    return ft
