#!/usr/bin/env python3 -i

# Simple Ex: A + s(B) + s(C + s(D)) + s(E + s(F) + s(G + s(H)))
# sqrt_solver = lambda M,N: (M%2 == 0, N%4 == 0, m := M//2, n := N//4, D := m*m - n, d := isqrt(D) if D >= 0 else -1, d*d == D, B := m+d, A :=m*m-B, (A,B) if 2*m == M and 4*n == N and D == d*d else None)
### A,B = sqrt_solver(M, N) where sqrt(M + sqrt(N)) = A + sqrt(B)

from fractions import Fraction as F
from decimal import Decimal as Dec, getcontext as gc; gc().prec=30; s = lambda x: Dec(str(x)).sqrt()
from math import gcd, sin, cos, pi
from functools import reduce

E = lambda x:(str(eval(x)), x)
#oddeven = lambda n: (e := len(bin(n ^ (n-1)))-3, o := n >> e)[::-1]
oddeven = lambda n: (e := len(f'{n^(n-1):b}')-1, o := n >> e)[::-1]

# bits: express v as n-bit string
#bits = lambda v,n:bin(v & 2**n-1)[2:].zfill(n)
bits = lambda v,n: f'{v&(2**n-1):0{n}b}'

# rep2x: Replace bit-string to radical expression: from 0/1 to +/- sqrt
rep2x = lambda bs:bs.replace("1","-s(2").replace("0","+s(2") + ")"*len(bs) + '/2'

# Sign for cos using Quadrant and Acute angle with X-axis
ST = lambda p,q: ( Q := (2*p//q) & 3, A := (p := p % (2*q), q-p, p-q, 2*q-p)[Q], S := Q == 1 or Q == 2, ('+-'[S], A) )[-1]
ST1 = lambda p,q: ( A := (p := p % (2*q), q-p, p-q, 2*q-p)[Q := (2*p//q) & 3], '+-'[Q == 1 or Q == 2] )[::-1]

# cos(pi * p/2**n) where p = odd and n >= 0
cospn = lambda p,n:rep2x(bits(p//2 ^ p//4, n-1)) if n > 1 else '0' if n == 1 else str(1-2*(p&1))

# cos(pi/3 * p/2**n) where p = odd and p%3 != 0 and n >= 0
cospe3 = lambda p,e: cospn(p*2//3, e+1).replace('(2)', '(3)') if e > 0 else '%cs(1)/2' % '-+'[p&1]

# cos(p, q) where q = m << n == odd << even

# cos(pi/o * p/2**e) where p = odd and e >= 0 and o > 4 and gcd(p, o) == 1
cospeo = lambda p,e,o: (st := ST(p, o), s := st[0], t := st[1], f := cospn(p*2//o, e+1).replace('(2)', f'(2{s}2*cos(pi * %s))') if e > 0 else f'{s}cos(pi * %s)', (f, (t,o), f % f'{t}/{o}') )[-1] 
#poe=lambda p,o,e: (E(f'cos(pi * {p}/({o}<<{e}))'), E(f'E(cospoe({p},{o},{e}))'))

#print("Try: p,q = 19, (2**32-1) // 17; T = fpSplit(p,q); p,q, sum([F(*t) for t in T[1]]) if T != None else None, T")

def DM(a,b): # divmod minimizing absolute value of remainder
    d,m = divmod(a,b)
    return (d+1, m-b) if 2*m > b else (d,m)

def fpSplit(p, q, T=True): # Partial Fractions into Fermat Prime Factors
    '''Splits a rational p/q into fermat prime rationals a/3 + b/5 + c/17 + d/257 + e/65537'''
    pp, qq = p, q # Original arguments for display
    N, D = [-2, 1, 4, 2, 64, 32768], (1, 3, 5, 17, 257, 65537)

    if q == 0:
       print("Error: Divide by 0")
       return None

    g = gcd(p, q)
    p, q = (p // g, q // g) if q > 0 else (p // -g, q // -g)
    if T: p %= 2*q # Trigonometric adjustment to rational angle

    o,e = oddeven(q)
    q = o

    if 0xFFffFFff % q != 0:
        p2 = '/2**%s'%e if e > 0 else ''
        print(' >>> cos(pi * %s/%s) == cos(pi%s * %s/%s)' % (pp,qq, p2,p,q))
        print('Error: 0xFFffFFff %% %s = %s != 0 (fermat prime split does not exist)' % (q, 0xFFffFFff % q))
        return None

    n = p * 0xFFffFFff//q
    d, m = divmod(n, 2**32-1)
    dmt  = [ DM(t[0]*m, t[1]) + (t[1],) for t in zip(N, D) ]
    d += sum([dm[0] for dm in dmt ])
    ft = [ (dm[1], dm[2]) for dm in dmt[1:] if dm[1] != 0 ]
    if d != 0: ft = [(d, 1)] + ft

    if 0:
        s = ' + '.join([ 'F(%s, %s)' % (a,b) for a,b in ft ])
        cmd = '2**%s * F(%s, %s) == F(%s, 2**32-1) == %s' % (e, pp,qq, n, s)
        print('Check (%s): %s' % (eval(cmd), cmd))
        s = ' + '.join([ '%s/%s' % (a,b) for a,b in ft ])
        p2 = '/2**%s'%e if e > 0 else ''
        print(' >>> cos(pi * %s/%s) == cos(pi%s * %s/%s) == cos(pi%s * (%s))' % (pp,qq, p2,p,q, p2,s))

    fts = '(%s)' % (' + '.join([ '%s/%s' % t for t in ft ]))
    return (e, ft, fts)

def S(p, q=180):
    if q == 0:
        return (None, 'Error: Divide by 0')
    print('Check: %s = sin(pi * %s/%s)' % (sin(pi*p/q), p, q))
    return C(q-2*p,2*q)

def C(p,q=180, dbg=False):
    if q == 0:
        return (None, 'Error: Divide by 0')
    print('Check: %s = cos(pi * %s/%s)' % (cos(pi*p/q), p, q))

    if q < 0:
        if dbg: print(' >>> Negative Denominator: %s / %s == %s / %s' % (p,q, -p,-q))
        p, q = -p, -q

    if (g := gcd(p, q)) > 1:
        pp, qq = p//g, q//g
        if dbg: print(' >>> Common Factors: %s / %s == %s / %s' % (p,q, pp,qq))
        p, q = pp, qq

    if p < 0 or p >= 2*q:
        pp = p % (2*q)
        if dbg: print(' >>> Periodic Function: cos(pi * %s/%s) == cos(pi * %s/%s)' % (p,q, pp,q))
        p = pp

    m, n = oddeven(q) # q == (m << n)
    r = 'cos(pi/2**%s * %s/%s)' % (n,p,m)
    print(' = %s = %s' % (str(eval(r)), r))

    # Permute 3 Cases: (n > 0) vs. (0xFFffFFff % m != 0) vs. (m not in [1, 3, 5, 17, 257, 65537])

    if (rr := 0xFFffFFff % m) != 0:
        if n > 0: # m = odd > 5
            if dbg: print(' >>> Even Denominator: %s == %s << %s' % (q, m, n))
            r = cospeo(p, n,m)[-1] # f, (t,o), r = cospeo(p, n,m)
            print(' = %s = %s' % (str(eval(r)), r))
        print('Error: 0xFFffFFff %% %s = %s != 0 (fermat prime split does not exist)' % (m, rr))
        return None

    if m < 4: # for both n >= 0
        r = cospe3(p, n) if m == 3 else cospn(p, n)
        print(' = %s = %s' % (str(eval(r)), r))
        return r

    # m >= 5 below
    f, (t,o), r = cospeo(p, n,m)
    print(' = %s = %s' % (str(eval(r)), r))
    if m not in [5, 17, 257, 65537]: # [1,3] excluded since m >= 5
        r = f % fpSplit(t, o)[-1]
        print(' = %s = %s' % (str(eval(r)), r))

    print('=====')
    # Perform exact value substition
    if m in [ 5, 15, 17, 51, 85, 255, 0xFFffFFff//17, 0xFFffFFff//15, 0xFFffFFff//5, 0xFFffFFff//3, 0xFFffFFff ]:
        if (cts := CT(p, m, n>0)) != None:
            if dbg: print(' >2> r = %s' % r)
            print(' = %s = %s' % (str(eval(r)), r))
            r = (cospn(p*2//m, n+1).replace('(2)', '(2%s)') if n>0 else '%s') % cts

    print(' = %s = %s' % (str(eval(r)), r))
    return r

# Use exact value lookup to return Cosine values
def CT(n,d, twice=False):
    '''Use exact value lookup to return Cosine values cos(pi * n/d)'''

    if (n := n % (2*d)) > d: n = 2*d - n
    sign, n = ('-',d-n) if 2*n > d else ('+', n)

    # Co-Prime Numerators for Fermat Prime (and multiple's) Denominators
    CPN = lambda q: [ n for n in range(q) if gcd(n,q) == 1 ]
    CPN2 = lambda q: [ n for n in range(1+q//2) if gcd(n,q) == 1 ]

    D = [ 5, 15, 17, 51, 85, 255, 0xFFffFFff//17, 0xFFffFFff//15, 0xFFffFFff//5, 0xFFffFFff//3, 0xFFffFFff ]
    T = [ '(+s(5)+1)/4',
          '(+s(30-s(180))+s(5)+1)/8',
          '(+1-s(17)+s(34-s(68)) + s(68+s(2448)+s(2720+s(6284288))))/16',
          '(-1-s(17)+s(34+s(68))+s(68-s(2448)+s(2720-s(6284288)))+s(408+s(9792)+s(19584+s(22560768))-s(39168-s(812187648)-s(902430720-s(691744975972466688)))))/32',
          '(+s((3-s(5))*(15-s(17)-s(34+s(68))-s(68-s(2448)-s(2720-s(6284288)))))+s((5+s(5))*(17+s(17)+s(34+s(68))+s(68-s(2448)-s(2720-s(6284288))))))/16',
          CT255 := 's(32 + s((18+s(20)+s(120-s(2880)))*(15+s(68+s(2448)-s(2720+s(6284288)))+s(34-s(68))+s(17))) + s((14-s(20)-s(120-s(2880)))*(17-s(17)-s(34-s(68))-s(68+s(2448)-s(2720+s(6284288))))))/8',
          # Tuples after d > 256
          (CT255,),
          (CT255x := '(+s((18+s(20)+s(120-s(2880)))*(15+s(68+s(2448)-s(2720+s(6284288)))+s(34-s(68))+s(17))) + s((14-s(20)-s(120-s(2880)))*(17-s(17)-s(34-s(68))-s(68+s(2448)-s(2720+s(6284288))))))/32', CT255),
          (CT255x, CT255), (CT255x, CT255), (CT255x, CT255)
    ]
    K = [ [1,2], [1,2,4,7], [1,2,3,4,5,6,7,8], [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 19, 20, 22, 23, 25, 26, 28, 29, 31, 32, 35, 37, 38, 40, 41, 43, 44, 46, 47, 49, 50], CPN(85), CPN2(255), 
          # Tuples after d > 256
          ([ 61465661 ], []),
          ([ 107107790, 179223363 ], [ 53553895 ]),
          ([ 122687581, 315963748, 543029711, 736305878 ], [ 157981874, 368152939 ]),
          ([ 220155544, 1211500221 ], [ 110077772, 365122018, 674826816 ]),
          ([ 793210282, 1690037549, 1951395068, 2343572227, 2604929746, 3501757013 ], [ 1243554653, 1302464873, 1325095783, 396605141, 964188671, 968910181, 975697534 ]),
          [ 'Error (unreachable code):  index -1 or out of range' ]
        ] 
    V = [ [0,1], [1,4,2,7], [ 80, 146, 7, 176, 15, 197, 37, 154 ],
# [ 80, 250, 7, 216, 15, 173, 37, 242 ],
# [202, 172, 7, 458, 23, 97, 353, 188],
        [50447, 3877, 9479, 45170, 39504, 1837, 29264, 37464, 52487, 20602, 11535, 59173, 20730, 22642, 37592, 61229, 1965, 31320, 45298, 47226, 4005, 50575, 47354, 9607, 31448, 39632, 61357, 29392, 22770, 52615, 59301, 11663], 
        [122375, 35501, 13554, 118287, 94288, 24792, 39589, 104997, 225360, 9466, 52879, 78962, 253447, 56967, 100909, 249359, 9722, 28880, 90200, 236069, 25048, 159952, 74874, 210034, 35757, 188039, 231981, 13810, 183951, 75130, 221272, 39845, 170661, 90456, 205946, 53135, 144626, 101165, 57223, 166573, 79218, 206202, 29136, 155864, 105253, 221528, 160208, 140538, 118543, 232237, 188295, 122631, 210290, 184207, 140794, 94544, 236325, 170917, 156120, 225616, 249615, 144882, 166829, 253703],
        [ 300026, 1061208, 955122, 1828871, 3813456, 912015, 1216882, 347053, 301050, 799448, 1787941, 3794959, 930512, 1173775, 478117, 348077, 1062232, 1656877, 3838066, 3140231, 1192272, 519047, 479141, 1217906, 800472, 1609850, 3682392, 3099301, 3401991, 2503632, 520071, 1174799, 956146, 1610874, 2968237, 3361061, 2485135, 2504656, 1193296, 913039, 1657901, 3683416, 2921210, 3229997, 2528242, 2486159, 3403015, 931536, 1788965, 3839090, 2922234, 3182970, 2372568, 2529266, 3362085, 3141255, 1829895, 3795983, 2969261, 3183994, 2373592, 3231021, 3100325, 3814480 ],
          # Tuples after d > 256
        ([ 587191 ], []),
        ([ 3442689, 1346561 ], [ 3442689 ]),
        ([ 852931, 2502729, 406601, 2951107 ], [ 2502729, 2951107 ]),
        ([ 1569340, 3667516 ], [ 1569340, 3716093, 3622588 ]),
        ([ 1819205, 2670658, 17429, 2113557, 574530, 3917381 ], [ 1013463, 574530, 2543881, 1819205, 2898163, 3636165, 17429 ])
    ]

    if d not in D: print('Error: d = %s NOT IN D = %s' % (d, D)); return None
    i = D.index(d)
    if d < 256:
        if n not in K[i]: print('Error: n = %s NOT IN K[i=%s] %s' % (n, i, K[i])); return None
        k = K[i].index(n);
        t = T[i].replace('+','%c').replace('-','%c');
        c = t.count('%c'); # 1,3,9
        v = V[i][k];
        #print('DBG 1: k, t, c, v = %s, %s, %s, %s' % (k,t,c,v))
    else:
        if n in K[i][0]:
            Ki, Ti, Vi = K[i][0], T[i][0], V[i][0]
        elif n in K[i][1]:
            Ki, Ti, Vi = K[i][1], T[i][1], V[i][1]
        else:
            print('Warning: n=%s is NOT IN K[i]=%s' % (n, K[i]))
            return None
        k = Ki.index(n);
        t = Ti.replace('+','%c').replace('-','%c');
        c = t.count('%c'); # 1,3,9
        v = Vi[k];
        #print('DBG: k, t, c, v = %s, %s, %s, %s' % (k,t,c,v))

    args = tuple(list(bin(v)[2:].zfill(c).replace('0','+').replace('1','-')))
    ret = sign + (t % args);

    print('Since: %ccos(pi*%s/%s) = %c%s = %s' % (sign,n,d, sign,cos(pi*n/d), '%s = %s'%E(ret)))
    return ret.replace('/4','/2').replace('/8','/4').replace('/16','/8').replace('/32','/16') if twice else ret;

def CTall(n=7):
    fp = [ 3, 5, 17, 257, 65537 ]
    fpDen = [reduce(lambda a,b:a*b,map(lambda t:t[0]**int(t[1]), zip([2**2**n+1 for n in range(4,-1,-1)],list(bin(m)[2:].zfill(5))))) for m in range(32)]
    ctAll = [ 'cos(pi * %s / %s) = %s' % (n, d, C(n, d)) for d in fpDen ]
    print("===\n" + "\n".join(ctAll) + "\n===\n")

# From https://en.wikipedia.org/wiki/Heptadecagon#Trigonometric_Derivation_using_nested_Quadratic_Equations
# import numpy as np; from math import pi, cos
# X = cos(pi/17)
# np.dot(CC := [32768, -131072, 212992, -180224, 84480, -21504, 2688, -128, 1], XX := [ (X:=cos(pi/17))**(2*n) for n in range(9) ][::-1] ) == -X

print('>>> CT255all(DD=255)')

def CT255all(DD=255):
    #DD = 255 # Generate all unique ( p, q, cosExp(pi * p/q) )
    tPQ = sorted([ F(n,DD).as_integer_ratio() for n in range(1,DD//2+1) ],key=lambda t:t[1])
    tPQC = [ (p, q, C(p,q)) for p,q in tPQ ]
    #for n,d in sorted([ f(n,DD).as_integer_ratio() for n in range(1,DD//2+1) ],key=lambda t:t[1]):
        #print(f'cos(pi * {n}/{d}) ')
    print("\n===\n")
    for i in range(len(tPQC)):
        n, d, c = tPQC[i]
        #print(f'{cos(pi * n/d)} = cos(pi * {n}/{d}) = {E(c)}')
        print(f'{i+1:3d}> cos(pi * {n}/{d}) = {cos(pi * n/d)} = {E(c)}')

print('>>> ST255all(DD=255)')

def ST255all(DD=255):
    #DD = 255 # Generate all unique ( p, q, cosExp(pi * p/q) )
    tPQ = sorted([ F(n,DD).as_integer_ratio() for n in range(1,DD//2+1) ],key=lambda t:t[1])
    tPQC = [ (p, q, S(p,q)) for p,q in tPQ ]
    #for n,d in sorted([ f(n,DD).as_integer_ratio() for n in range(1,DD//2+1) ],key=lambda t:t[1]):
        #print(f'cos(pi * {n}/{d}) ')
    print("\n===\n")
    for i in range(len(tPQC)):
        n, d, c = tPQC[i]
        #print(f'{cos(pi * n/d)} = cos(pi * {n}/{d}) = {E(c)}')
        print(f'{i+1:3d}> sin(pi * {n}/{d}) = {sin(pi * n/d)} = {E(c)}')

# SS = sympy.simplify
import sympy; SS = lambda x: str(sympy.simplify(x.replace('s','sqrt'))).replace('sqrt','s')

# Update +/- in any trig expression from binary integer representation
# e.g. nxfmt(1, '(1+s(5)+s(7))/6')
nxfmt = lambda n,x: ( f := x.replace('+','%c').replace('-','%c') ) % tuple(f'{n:0{f.count("%c")}b}'.replace('0\
','+').replace('1','-'))

