#!/usr/bin/env python3 -i 

from decimal import Decimal as Dec, getcontext as gc

# https://github.com/vishal--mishra/PiDigits/blob/master/pi.py3
# https://en.wikipedia.org/wiki/Chudnovsky_algorithm AND https://handwiki.org/wiki/Chudnovsky_algorithm

def PI(maxK: int = 70, prec: int = 1008, disp: int = 1007):  # Parameter defaults chosen to gain 1000+ digits within a few seconds
    gc().prec = prec
    K, M, L, X, S = 6, 1, 13_591_409, 1, 13_591_409
    for k in range(1, maxK + 1):
        M = (K**3 - 16*K) * M // k**3 
        L += 545_140_134
        X *= -262_537_412_640_768_000 # - 640_320 ** 3
        S += Dec(M * L) / X
        K += 12
    pi = 426_880 * Dec(10_005).sqrt() / S
    pi = Dec(str(pi)[:disp])  # Drop few digits of precision for accuracy
    #print("PI(maxK={} iterations, gc().prec={}, disp={} digits) =\n{}".format(maxK, prec, disp, pi))
    return pi

def main():
    Pi = PI()
    print("Pi = PI() = PI(70, 1008, 1007) # default params") 
    print("Pi = %s\n" % Pi)
    print("For greater precision and more digits (takes a few extra seconds) - Try")
    print("Pi = PI(317, 4501, 4500); print('Pi = %s' % Pi)") 
    print("Pi = PI(353, 5022, 5020); print('Pi = %s' % Pi)")

if __name__ == "__main__":
    main()
