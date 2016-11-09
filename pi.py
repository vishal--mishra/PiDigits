#!/usr/bin/env python -i

# Copyright (c) 2016 Vishal International Inc.
# Copyright (c) 2016 VishNet Systems Inc.

from decimal import *; from decimal import Decimal as Dec; #getcontext().prec = 1005; # 105
#from fractions import *; from fractions import Fraction as Frac; toDec = lambda f:Dec(f.numerator)/f.denominator

print "===";
print "Chudnovsky_algorithm - https://en.wikipedia.org/w/index.php?title=Chudnovsky_algorithm";
print "Pi (12 trillion) - http://www.numberworld.org/misc_runs/pi-12t/";
print "To Verify (Pi million): http://www.piday.org/million/";
print "===";
print "Mk = (6k)!/((3k)!*(k!^3)), Lk = 545,140,134*k+13,591,409 & Xk = (-640320^3)**k (MLX = Multinomial, Linear & Exponential terms)";
print "Pi = (426880 * 10005**.5) / Sum(Tk = Mk*Lk/Xk) where k=0:Inf";
print "Note: 640320^1.5 / 12 = (640320/12) * 800 * (1 + 320/640000)^.5 = 42688000 * 1.0005^.5";
print "===";

def PI(maxK=70, prec=1008, disp=1007):
    getcontext().prec = prec;
    k6,M,L,X,S = 0, 1, 13591409, 1, 13591409; # 0*6, 0!=1, 13591409, (-604320**3)**0, Dec(13591409);
    for k in xrange(1,maxK+1):
        M = M * 8 * (k6+1) * (k6+3) * (k6+5) / k**3; k6 += 6;
        #M = M * (k6+1) * (k6+3) * (k6+5) / k**3; k6 += 6;
        L += 545140134;
        X *= -262537412640768000 # -640320**3;
        #X *= -32817176580096000 # -320160**3;
        S += Dec(M)*L / X;
    pi = 426880 * 10005**Dec(".5") / S;
    print "PI(maxK=%d, getcontext().prec=%d, disp=%d) =\n%s" % (maxK, prec, disp, ("%s"%pi)[:disp]);

PI();
print "===";
print "PI(317,4501,4500)";
print "PI(353,5022,5020)";
print "Suggestion: prec=disp+~5 and maxK can be reduced while result does not change";
print "===";

if (0):
    factorial = lambda k:reduce(lambda a,b:a*b, range(1,k+1));
    fact = lambda k:factorial(k+1)/(k+1);
    Nk = lambda k:fact(6*k)/fact(3*k)/fact(k)**3*(545140134*k+13591409);
    Dk = lambda k:(-640320**3)**k;
    Tk = lambda k:Frac(Nk(k), Dk(k));
    #Sk = lambda n:toDec(reduce(lambda a,b:a+b, map(lambda k:Frac(Nk(k),Dk(k)),range(n+1))));
    Sk = lambda n:reduce(lambda a,b:a+b, map(lambda k:Dec(Nk(k))/Dk(k),range(n+1)));
    #Pi = lambda n:42688000*Dec("1.0005")**Dec(".5") / Sk(n);
    Pi = lambda n:426880 * 10005**Dec(".5") / Sk(n);
    print "getcontext().prec = 1005";
    print "Pi(70) = %s" % Pi(70);

