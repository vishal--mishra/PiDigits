#!/usr/bin/env python3 -i

import re;
from functools import reduce

# choose s as some sqrt function
# import math; s = math.sqrt;
from math import *; # s = sqrt; # from math import sqrt as s;
from decimal import Decimal as Dec, getcontext as gc; gc().prec=30; s = lambda r:Dec("%s"%r).sqrt()
from fractions import Fraction as Frac;
f,d = Frac, Dec

# Quadrants 0-3 for angle (pi * p/q) 
Q = lambda p,q: (2*p//q) & 3
AngX = lambda p,q: (p, q-p, p-q, 2*q-p)[Q(p,q)]

E = lambda x:(str(eval(x)), x)
sinD = lambda t:Dec(sin(t))
cosD = lambda t:Dec(cos(t))

# Safe Eval for arc cos (arc func)
def sE(sx,af=acos):
    try:
        ret = float(eval(sx))
        if abs(ret) > 1:
            return (None, ret)
        else:
            ret = round(af(ret)/pi * 0xFFffFFff, 5)
            if ret == int(ret):
                return frac(int(ret), 0xFFffFFff)
            else:
                return (None, ret)
    except: pass
    return (None, 'Eval sqrt Error')

sES = lambda sx:sE(sx, asin)

# frac: Reduce a fraction to positive terms with period 2
def frac(n,d): f=Frac(n,d); return (f.numerator % (2*f.denominator), f.denominator)
def quad(n,d): p,q=frac(n,d); return (2*p // q)
def qAng(n,d): u,v=frac(n,d); q = 2*u//v; a = [u, v-u, u-v, 2*v-u][q]; return ((u,v), q, (a,v))

# Split number into odd and power of 2
def oddeven(n): m = int(log(((n^(n-1))),2)-0.5); return (n>>m, m)

# Cos subtraction Formula
#fmin = lambda t1,t2: (f1:=Frac(*t1), f2:=Frac(*t2), f3 := (f1-1,f2-1) if f1>1 and f2>1 else (f1,f2), ((f3[0].numerator, f3[0].denominator), (f3[1].numerator, f3[1].denominator)) )[-1]
fmin = lambda t1,t2: (f1:=Frac(*t1), f2:=Frac(*t2), f3 := (f1-1,f2-1) if f1>1 or f2>1 else (f1,f2), ((f3[0].numerator, f3[0].denominator), (f3[1].numerator, f3[1].denominator)) )[-1]
csub = lambda p,q: (f:=frac(p,q), oe := oddeven(f[1]), d:=fpDict[oe[0]], f1:=frac(p*d[0][0],d[0][1]), f2:=frac(p*d[1][0],d[1][1]), "(%s*%s/%s - %s*%s/%s)"%((p,)+d[0]+(p,)+d[1]), "(%s/%s - %s/%s)"%(f1+f2), f3:=fmin(f1,f2), "(%s/%s - %s/%s)"%(f3[0]+f3[1]) )
CSub = lambda p,q: (cs := csub(p,q), f"cos(pi*{p}/{q}) = cos(pi*{cs[-4]}) = cos(pi*{cs[-3]}) = cos(pi*{cs[-1]})")[-1]

# cos(2*pi/3) = -cos(pi/3) = -1/2
# sin(2*pi/3) = sin(pi/3) = s(3)/2

# 4cos(2*pi/5) = s(5)-1 and 4cos(pi/5)=s(5)+1

# 010: cos = -++ and sin = -+-
# cos(2*pi/15) = cos(pi/3-pi/5) = (s(30-s(180))+s(5)+1)/8 = 0.913545457642600895502127571985
# sin(2*pi/15) = sin(pi/3-pi/5) = (s(15)+s(3)-s(10-s(20)))/8 = 0.406736643075800207753985990341

# 100: cos = +-+ and sin = ++-
# cos(4*pi/15) = cos(2*pi/3-2*pi/5) = (s(30+s(180))-s(5)+1)/8 = 0.669130606358858213826273330688 
# sin(4*pi/15) = sin(2*pi/3-2*pi/5) = (s(10+s(20))+s(15)-s(3))/8 = 0.743144825477394235014697048974

# 111: cos = --- and sin = -++
# cos(7*pi/15) = -cos(4*pi/3-4*pi/5) = (s(30-s(180))-s(5)-1)/8 = 0.104528463267653471399834154802
# sin(7*pi/15) = +sin(4*pi/3-4*pi/5) = (s(10-s(20))+s(15)+s(3))/8 = 0.994521895368273336922691944981

# 001: cos ++- and sin = +-+
# cos(pi/15) = -cos(8*pi/3-8*pi/5) = (s(30+s(180))+s(5)-1)/8 = 0.97814760073380563792856674787
### = s(7-s(30-s(180))-s(5))/4
# sin(pi/15) = -sin(8*pi/3-8*pi/5) = (s(10+s(20))-s(15)+s(3))/8 = 0.207911690817759337101742284406

# cos(pi*64/255) = (s((1+(s(30+s(180))-s(5)+1)/8)*(1+(-(s(34-s(68))-s(17)+1) + 2*s(s(34-s(68))+s(17)-1)*s(s((17+s(272)))))/16))-s((1-(s(30+s(180))-s(5)+1)/8)*(1-(-(s(34-s(68))-s(17)+1) + 2*s(s(34-s(68))+s(17)-1)*s(s((17+s(272)))))/16)))/2

# for n in [1,2] => n-1 = [0,1]
sinp5 = lambda n: 's(10%cs(20))/4' % tuple(['-', '+'][n-1])
cosp5 = lambda n: '(s(5)%c1)/4' % tuple(['+', '-'][n-1])

# for n in [1,2,4,7] => n/2 = [0,1,2,3]
sinp15 = lambda n:'(%cs(10%cs(20))%cs(15)%cs(3))/8' % tuple(['++-+', '--++', '+++-', '+-++'][n//2])
cosp15 = lambda n:'(s(30%cs(180))%cs(5)%c1)/8' % tuple(['++-', '-++', '+-+', '---'][n//2])
#cospn15 = cosp15

# Cos of Sum/Difference with +/- sign of both terms
CSD = lambda cx1,sgn,cx2: '(%cs((1+%s)*(1+%s))%cs((1-%s)*(1-%s)))/2' % (sgn[0], cx1, cx2, sgn[1], cx1, cx2)
#print('cos(pi*64/255) == E(CSD(C(4,15), "+-", C(4,17)))')
    
# bits: express v as n-bit string
#bits = lambda v,n:bin(v & 2**n-1)[2:].zfill(n)
bits = lambda v,n: f'{v&(2**n-1):0{n}b}'

# rep2x: Replace bit-string to radical expression: from 0/1 to +/- sqrt
rep2x = lambda bs:bs.replace("1","-s(2").replace("0","+s(2") + ")"*len(bs) + '/2'

# rcos: radical form cos function: odd p & n>1
cospn = lambda p,n:rep2x(bits(p//2 ^ p//4, n-1))

def S(p,q):
    if q == 0: 
        print("Error: Divide by 0")
        return None
    p,q = frac(p,q);
    if q == 5:
        return sinp5(p)
    if q == 15:
        return sinp15(p)
    if q == 17:
        sign = '+' if 2*p//q < 2 else '-'
        if 2*p < 34:
            if 2*p > 17:
                p = 17-p
        else:
            if 2*p > 51:
                p = 34 - p
            else:
                p = p - 17
        if p in range(1,9):
            return sign + S17(p)
    m,n = frac(q-2*p,2*q);
    print("sin(pi*%s/%s) = %s = cos(pi*%s/%s)\n =" % (p,q,sin(pi*p/q),m,n),)
    return C(m,n);

def C(p,q):
    if q == 0: 
        print("Error: Divide by 0")
        return None
    p,q = frac(p,q);
    m,n = oddeven(q);
    print("cos(pi*%s/%s) = %s = cos(pi/2**%s * %s/%s)" % (p,q,cos(pi*p/q),n,p,m))
    t = p % (2*m);
    sign,t = [('+',t), ('-',m-t), ('-',t-m), ('+',2*m-t)][2*t//m] # s=sign, t=theta
    if m>2:
        r = C2(p*2//m,n+1).replace('(2)', '(2%c2*cos(pi*%s/%s))'%(sign,t,m)) if n>0 else '%ccos(pi*%s/%s)' % (sign,t,m)
        print(' = ~ %s = %s' % (str(eval(r)), r))
        if m in [5,15,17]:
            print("Note:",)
            CT(t,m)
    if (0xFFffFFff % m != 0):
        print("Error: No radical form solution exists: 0xFFffFFff %% %s = %s != 0" % (m, 0xFFffFFff % m))
        return None;
    if m == 1: r=C2(p,n); print(' = %s = %s' % (str(eval(r)), r)); return r
    if m == 3: r=C3(p,n); print(' = %s = %s' % (str(eval(r)), r)); return r
    if m == 5: r=C5(p,n); print(' = %s = %s' % (str(eval(r)), r)); return r
    if m == 15: r=C15(p,n); print(' = %s = %s' % (str(eval(r)), r)); return r
    if m == 17: r=C17(p,n); print(' = %s = %s' % (str(eval(r)), r)); return r
    if m in [51,85,255]: r=C255(p*255//m,n); print(' = %s = %s' % (str(eval(r)), r)); return r
    #r = C2(p*2/m,n+1).replace('(2)', '(2+2*cos(pi*%s/%s))'%(p%(2*m),m)) if n>0 else 'cos(pi*%s/%s)' % (p,m)
    #r = C2(p*2//m,n+1).replace('(2)', '(2%c2*cos(pi*%s/%s))'%(sign,t,m)) if n>0 else '%ccos(pi*%s/%s)' % (sign,t,m)
    r = C2(p*2//m,n+1).replace('(2)', '(2%c2*cosD(pi*%s/%s))'%(sign,t,m)) if n>0 else '%ccosD(pi*%s/%s)' % (sign,t,m)
    print(' = %s = %s' % (str(eval(r)), r))
    return r

def C2(p,n):
    if n<0: return '1'
    if n==0: return str(1 - 2*(p&1))
    if n==1: return '0'
    return cospn(p, n)

def C3(p,n): 
    #if n == 0: return '+1./2' if (p&1)==1 else '-1./2'
    if n == 0: return '+s(1)/2' if (p&1)==1 else '-s(1)/2'
    return C2(p*2//3,n+1).replace('(2)','(3)')

def C5(p,n):
    if n == 0:
        p = p % 10;
        if p == 1: return '(s(5)+1)/4'
        if p == 2: return '(s(5)-1)/4'
        if p == 3: return '-'+C5(2,0);
        if p == 4: return '-'+C5(1,0);
        else: return C5(10-p,0);
    k = p%10; # 1,2 3,4 6,7 8,9
    if k in [3,4,6,7]:
        #return C2(p*2//5,n+1).replace('(2)', '(2-2*cos(pi*%s/5))'%(abs(k-5)));
        k = abs(k-5)
        if k == 1:
            return C2(p*2//5,n+1).replace('(2)', '(2-(s(5)+1)/2)');
        if k == 2:
            return C2(p*2//5,n+1).replace('(2)', '(2-(s(5)-1)/2)');
    else: # k in [1,2,8,9]
        if k in [8,9]:
            k = 10-k
        #return C2(p*2//5,n+1).replace('(2)', '(2+2*cos(pi*%s/5))'%(k));
        if k == 1:
            return C2(p*2//5,n+1).replace('(2)', '(2+(s(5)+1)/2)');
        if k == 2:
            return C2(p*2//5,n+1).replace('(2)', '(2+(s(5)-1)/2)');
    # return C2(p*2//5,n+1).replace('(2)', '(2%c(s(5)%c1)/2)'%(t[0],t[1]));

def C15(p,n):
    if n == 0:
        if p in [1,2,4,7]:
            return cosp15(p)
        m = 15; t = p % (2*m)
        sign,t = [('+',t), ('-',m-t), ('-',t-m), ('+',2*m-t)][2*t//m] # s=sign, t=theta
        return '%c%s' % (sign, C15(t,0))

    m = 15; t = p % (2*m)
    sign,t = [('+',t), ('-',m-t), ('-',t-m), ('+',2*m-t)][2*t//m] # s=sign, t=theta
    return C2(p*2//15,n+1).replace('(2)', '(2%c%s)'%(sign, C15(t,0).replace('/8','/4')));

def C17(p, n):
    if n == 0 and p in range(1,9):
        return '(-1+s(17)+s(34-s(68)) + s(68+s(2448)-s(2720+s(6284288))))/16'.replace('+','%c').replace('-','%c') % tuple(list(bin([80,146,7,176, 15,197,37,154][p-1])[2:].zfill(8).replace('0','+').replace('1','-')))
        return '(+(s(34-s(68))+s(17)-1) + 2*s(s(34-s(68))-s(17)+1)*s(s((17+s(272)))))/16'.replace('+','%c').replace('-','%c') % tuple(list(bin([202, 172, 7, 458, 23, 97, 353, 188][p-1])[2:].zfill(9).replace('0','+').replace('1','-')))
        # Templatize cos(pi*2/17) and substitute bit pattern of numerator in range 1..8
        C2_17 = '(+(s(34-s(68))+s(17)-1) + 2*s(s(34-s(68))-s(17)+1)*s(s((17+s(272)))))/16'
        T17 = C2_17.replace('+','%c').replace('-','%c');
        V17 = [(1, 202), (2, 172), (3, 7), (4, 458), (5, 23), (6, 97), (7, 353), (8, 188)]
        return T17%tuple(list(bin(V17[p-1][1])[2:].zfill(9).replace('0','+').replace('1','-')))

    m = 17; t = p % (2*m)
    sign,t = [('+',t), ('-',m-t), ('-',t-m), ('+',2*m-t)][2*t//m] # s=sign, t=theta
    #r = C2(p*2//m,n+1).replace('(2)', '(2%c2*(%s))'%(sign,C17(t,0))) if n>0 else '%c(%s)' % (sign,C17(t,0))
    r = C2(p*2//m,n+1).replace('(2)', '(2%c%s)'%(sign,C17(t,0))).replace('/16','/8') if n>0 else '%c(%s)' % (sign,C17(t,0))
    return r

def S17(p): # 1 <= p <= 8, n == 0
    if p in range(1,9):
        return 's(34-s(68)+s(136-s(1088))-s(272+s(39168)+s(43520+s(1608777728))))/8'.replace('+','%c').replace('-','%c') % tuple(list(bin([122,88,45,114, 37,15,7,80][p-1])[2:].zfill(7).replace('0','+').replace('1','-')))

def C255(p,n):
    #return 'cos(pi*%s/%s)' % (p,n)
    if n == 0:
        if (p%5 == 0): return CC255(p//5, 51)
        if (p%3 == 0): return CC255(p//3, 85)
        return CC255(p, 255)
        if p%2 == 0:
            print(' = cos(pi*%s/15 - pi*%s/17)' % (p/2, p/2))
            return 'cos(pi*%s/15 - pi*%s/17)' % (p/2, p/2)
        else:
            print(' = s(2 + 2*cos(pi*%s/15 - pi*%s/17))/2' % (p, p))
            return 's(2 + 2*cos(pi*%s/15 - pi*%s/17))/2' % (p, p);
    m = 255; t = p % (2*m)
    sign,t = [('+',t), ('-',m-t), ('-',t-m), ('+',2*m-t)][2*t//m] # s=sign, t=theta
    r = C2(p*2//m,n+1).replace('(2)', '(2%c2*(%s))'%(sign,C255(t,0))) if n>0 else '%c(%s)' % (sign,C255(t,0))
    return r

def C257(p,n):
    return 'cosD(pi*%s/%s)' % (p,n)

def C65535(p,n):
    return 'cosD(pi*%s/%s)' % (p,n)

def C65537(p,n):
    return 'cosD(pi*%s/%s)' % (p,n)

def C0xFFffFFff(p,n):
    return 'cosD(pi*%s/%s)' % (p,n)

# Fermat Prime Denominators
#fpDen = [reduce(lambda a,b:a*b,map(lambda t:t[0]**int(t[1]), zip([2**2**n+1 for n in range(4,-1,-1)],list(bin(m)[2:].zfill(5))))) for m in range(1,32)]
fpDen = [reduce(lambda a,b:a*b,map(lambda t:t[0]**int(t[1]), zip([2**2**n+1 for n in range(4,-1,-1)],list(bin(m)[2:].zfill(5))))) for m in range(32)]
#print('fpDen =', fpDen)
ff1=list(zip([sum(map(lambda n:int(n), list(bin(n)[2:].zfill(5)))) for n in range(32)],fpDen))
ff1.sort();

if 0:
    print('There are 5 Fermat primes so they can be combined into 2**5=32=1+5+10+10+5+1 combinations of odd denominators')
    print(" *  1: %s" % [ t for t in ff1 if t[0]==0 ])
    print(" *  5: %s" % [ t for t in ff1 if t[0]==1 ])
    print(" * 10: %s" % [ t for t in ff1 if t[0]==2 ])
    print(" * 10: %s" % [ t for t in ff1 if t[0]==3 ])
    print(" *  5: %s" % [ t for t in ff1 if t[0]==4 ])
    print(" *  1: %s" % [ t for t in ff1 if t[0]==5 ])

#print('1 == 3*2-5 == 3*6-17 == 3*86-257 == 3*21846-65537 == 5*7 - 17*2 == 5*103 - 257*2 == 5*26215 - 65537*2 == 17*121 - 257*8 == 17*30841 - 65537*8 == 257*32641 - 65537*128')
# Weight for unit difference
wtud = {
    (3,5): (2,1), (3,17): (6,1), (3,257): (86,1), (3,65537): (21846,1), (5,17): (7,2), (5,257): (103,2), (5,65537): (26215,2), (17,257): (121,8), (17,65537): (30841,8), (257,65537): (32641,128),
    (15,17): (16/2,16/2-1), (255,257): (256/2,256/2-1), (65535,65537): (65536/2,65536/2-1)
}
#print('wtud = ', wtud)
#print([ t[0][0]*t[1][0] - t[0][1]*t[1][1] for t in zip(wtud.keys(), wtud.values())])
wtudd = dict([ (k[0]*k[1], k) for k in wtud.keys() ])
#print('wtudd =', wtudd)
#print('1 == 15*8 - 17*7 = 255*128 - 257*127 == 65537*32768 - 65535*32769')

ff = lambda q: (wtudd[q], wtud[wtudd[q]])
gg = lambda p,ffq: ((p*ffq[1][0]%(2*ffq[0][1]), ffq[0][1]), (p*ffq[1][1]%(2*ffq[0][0]), ffq[0][0]))

def TT(p,q):
    if q in wtudd.keys():
        (a,b),(c,d) = gg(p, ff(q))
        print('cos(pi* %d/%d) = cos(pi*%d/%d - pi*%d/%d))' % (p,q, a,b, c,d))
        ret = '((%s)*(%s) + (%s)*(%s))' % (C(a,b), C(c,d), S(a,b), S(c,d))
        ret = ret.replace('1.', 'Dec(1)')
        print('ret  =', ret)
        print(' => %s ?= %s' % (cos(pi*p/q), eval(ret)))
        return ret

fpXgcd = lambda a,b: ((Y := (a-1)//2, a), (X := (1 + b*Y)//a, b))[::-1]
fp = [ 3, 5, 17, 257, 65537 ]
fp2Dict = { a*b : fpXgcd(a,b) for a in fp for b in fp if a < b }
fp2Dict = dict(sorted(fp2Dict.items()))
if 0:
    print("===\nfp2Dict = %s\n(a,b)" % fp2Dict)
    print("\n".join([ ' . cos(pi * n/%s) = cos(pi * (n*%s/%s - n*%s/%s)) = C1*C2 + S1*S2' % (k, *sum(fp2Dict[k], ())) for k in fp2Dict ]))

fp3Dict = { a*b*c : fpXgcd(a*b,c) for a in fp for b in fp for c in fp if a < b < c }
fp3Dict = dict(sorted(fp3Dict.items()))
if 0:
    print("===\nfp3Dict = %s\n(a*b,c)" % fp3Dict)
    print("\n".join([ ' . cos(pi * n/%s) = cos(pi * (n*%s/%s - n*%s/%s)) = C1*C2 + S1*S2' % (k, *sum(fp3Dict[k], ())) for k in fp3Dict ]))

fp4Dict = { a*b*c*d : fpXgcd(a*b*c,d) for a in fp for b in fp for c in fp for d in fp if a < b < c < d }
fp4Dict = dict(sorted(fp4Dict.items()))
if 0:
    print("===\nfp4Dict = %s\n(a*b*c,d)" % fp4Dict)
    print("\n".join([ ' . cos(pi * n/%s) = cos(pi * (n*%s/%s - n*%s/%s)) = C1*C2 + S1*S2' % (k, *sum(fp4Dict[k], ())) for k in fp4Dict ]))

fp5Dict = { a*b*c*d*e : fpXgcd(a*b*c*d,e) for a in fp for b in fp for c in fp for d in fp for e in fp if a < b < c < d < e }
fp5Dict = dict(sorted(fp5Dict.items()))
if 0:
    print("===\nfp5Dict = %s\n(a*b*c*d,e)" % fp5Dict)
    print("\n".join([ ' . cos(pi * n/%s) = cos(pi * (n*%s/%s - n*%s/%s)) = C1*C2 + S1*S2' % (k, *sum(fp5Dict[k], ())) for k in fp5Dict ]))

fpDict = fp2Dict | fp3Dict | fp4Dict | fp5Dict
fpDict = dict(sorted(fpDict.items()))
if 0:
    print("===\nfpDict = %s" % fpDict)
    print("\n".join([ ' . cos(pi * n/%s) = cos(pi * (n*%s/%s - n*%s/%s)) = C1*C2 + S1*S2' % (k, *sum(fpDict[k], ())) for k in fpDict ]))

print("===")
fCC = lambda d: (d, t := fpDict[d], 'C(1, %s) = C(Frac%s - Frac%s) = C%s * C%s + S%s * S%s' % (d, *t, *t, *t))
fSS = lambda d: (d, t := fpDict[d], 'S(1, %s) = S(Frac%s - Frac%s) = S%s * C%s - S%s * C%s' % (d, *t, *t, *t))
fTT = lambda d: (d, ttt := fpDict[d], t := (ttt[0]+ttt[1])*2,  'cos(pi*1/%s) == cos(pi*%s/%s) * cos(pi*%s/%s) + sin(pi*%s/%s) * sin(pi*%s/%s)' % (d, *t))
fTT(5*257)
# cos(pi*103/257) * cos(pi*2/5) + sin(pi*103/257) * sin(pi*2/5)
# ttt = fpDict[1285]; (ttt[0]+ttt[1])*2

fqq = lambda q:bin(q)[2:].zfill(2)[-2]
fUU = lambda n,d: (f := fpDict[d], t1 := f[0], t2 := f[1], q1 := quad(n*t1[0], t1[1]), q2 := quad(n*t2[0], t2[1]), sc := '+-'[fqq(q1+1) != fqq(q2+1)], ss := '+-'[fqq(q1) != fqq(q2)], f'CSD(C(2*{n}*{t1[0]},{t1[1]}), "{sc}{ss}", C(2*{n}*{t2[0]},{t2[1]}))', f'cos(pi*{n}/{d})')

def CC255(n, d):
    tup = fUU(n,d); r1=E(tup[-1]); r2=E(tup[-2]);
    t1,t2=fpDict[d]; exp1='cos(pi*(%s*%s/%s - %s*%s/%s))'%(n,*t1, n,*t2);
    exp2 = '[+/- s( (1+cos2A)*(1+cos2B) ) +/- s( (1-cos2A)*(1-cos2B) )]/2'
    print(r1, r2); print(f"\n{r1[1]} = {r1[0]} = %s = %s\n = %s = {r2[1]} = {r2[0]}\n" % (exp1, exp2, eval(r2[0]))) 
    #return r2[0]
    return r2[0].replace('++','+').replace('--','+').replace('+-','-').replace('-+','-')

if 0:
    tup4 = fUU(64, 255);
    print(tup4)
    print(f'({tup4[-1]}, {tup4[-2]})')

print('Example: E(C(17,3<<4))')
print(E(C(17,3<<4)))
if False:
    C2_17 = '(+(s(34-s(68))+s(17)-1) + 2*s(s(34-s(68))-s(17)+1)*s(s((17+s(272)))))/16'
    T17 = C2_17.replace('+','%c').replace('-','%c');
    print("Template (cos(pi/17*N)) = T17 = '%s'" % T17)
    V17 = [(1, 202), (2, 172), (3, 7), (4, 458), (5, 23), (6, 97), (7, 353), (8, 188)]
    print("Template Values (cos(pi/17*N)) = V17 = '%s'" % V17)
    cc17 = lambda n:T17%tuple(list(bin(V17[n-1][1])[2:].zfill(9).replace('0','+').replace('1','-')))
    print('cc17(1) = %s' % cc17(1))
    print([ round(acos(float(eval(cc17(n))))*17/pi,14) for n in range(1,9) ])
print([ (round(acos(float(eval(C17(p,0))))*17/pi,14), C17(p,0)) for p in range(1,9) ])
#print([ C(n,17) for n in range(1,9)])

D = [5, 15, 17]
T = ['(+s(5)+1)/4', '(+s(30-s(180))+s(5)+1)/8', '(+(s(34-s(68))+s(17)-1) + 2*s(s(34-s(68))-s(17)+1)*s(s((17+s(272)))))/16' ]
TS = ['(+s(10+s(20))/4', '(s(15)+s(3)-s(10-s(20)))/8', '(+(s(34-s(68))+s(17)-1) + 2*s(s(34-s(68))-s(17)+1)*s(s((17+s(272)))))/16' ]
K = [ [1,2], [1,2,4,7], [1,2,3,4,5,6,7,8] ]
V = [ [0,1], [1,4,2,7], [202, 172, 7, 458, 23, 97, 353, 188] ]

def CT(n,d):
    i = D.index(d) if d in D else -1;
    if i == -1 or n not in K[i]: return None
    k = K[i].index(n);
    t = T[i].replace('+','%c').replace('-','%c');
    c = t.count('%c'); # 1,3,9
    v = V[i][k];
    args = tuple(list(bin(v)[2:].zfill(c).replace('0','+').replace('1','-')))
    ret = t % args;
    print('cos(pi*%s/%s) = %s = %s' % (n,d,cos(pi*n/d), '%s = %s'%E(ret)))
    return ret;

print('Try: CT(1,5)')
print('===')

# Reverse search all rational multiples of pi for which +/- replacement of this expression works
def RS(sx,af=acos): # sx = string expression; x = eval(sx)
    #print('RS(sx=%s)' % sx)
    fmt = sx.replace('+', '%c').replace('-','%c');
    argc = fmt.count('%c')
    exps = [ (n, fmt%tuple(list(bin(n)[2:].zfill(argc).replace('0','+').replace('1','-')))) for n in range(2**argc)]
    evl = [ (t[0], sE(t[1],af), t[1]) for t in exps if sE(t[1],af)[0] != None ]
    #print(evl)
    #evl.sort(cmp=lambda x,y:0 if x[1]==y[1] else +1 if x[1]>y[1] else -1)
    evl.sort(key=lambda obj:obj[1]) # cmp=lambda x,y:0 if x[1]==y[1] else +1 if x[1]>y[1] else -1)
    for ct in evl:
        if (af == acos):
            print(E('cos(pi * %s/%s)'%ct[1]) + (ct[0],) + E(ct[2]))
        else:
            print(E('sin(pi * %s/%s)'%ct[1]) + (ct[0],) + E(ct[2]))

        #print('QQQ =', ct)
        #if ct[1][0] != None:
            #print(E('sin(pi * %s/%s)'%ct[1]) + (ct[0],) + E(ct[2]))

#RS('(s(30-s(180))+s(5)+1)/8')
#print('Try: RS("(+(s(34-s(68))+s(17)-1) + 2*s(s(34-s(68))-s(17)+1)*s(s((17+s(272)))))/16")')

#[ RS(x) for x in (['+1./2']+T) ]
#[ RS(x,asin) for x in (['+s(3)/2']+TS) ]
print('===')
RS('(-1+s(17)+s(34-s(68)) + s(68+s(2448)-s(2720+s(6284288))))/16')
print('===')

print('cos(pi/51) = (s(3)*(%s)+(%s))/2' % (S(6,17), C(6,17)))
print('E(CSD(C(4,15), "+-", C(4,17)))[0], cos(pi*64/255)')

def CT255():
    ct255 = [ (n, C(n,255)) for n in range(1,255) ]
    print("\n", [ RS(x) for x in (['+s(1)/2']+T) ])
    print("\ncos( pi/255 *", [ round(acos(float(eval(ct255[n][1])))*255/pi, 9) for n in range(254) ], ")")

print("Run> CT255()")

def CTall(n):
    print("\n".join([ CSub(n,d) for d in sorted(set(fpDen) - set(fp) - {1}) ]))

print("Run> CTall(23)")

An,Ap = 's(34-s(68))', 's(34+s(68))'; Bp,Bn = '(s(17)+1)', '(s(17)-1)'; Cn,Cp = 's(s(17-s(272)))', 's(s(17+s(272)))'
print([ round(asin(float(eval(S17(n))))*17/pi,8) for n in range(1,9) ])
