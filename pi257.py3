#!/usr/bin/env python3 -i

# Calculating radical form expression for cos(2^n * pi / 257)

from math import *;
from decimal import Decimal as Dec, getcontext as gc; gc().prec=30; s = lambda r:Dec(r).sqrt()

Q = lambda b,c:((b+s(b*b-4*c))/2, (b-s(b*b-4*c))/2)

t0,t1 = Q(-1,-64); t = [t0, t1];
(z0,z2), (z1,z3) = Q(t0,-16), Q(t1,-16); z = [z0,z1,z2,z3];

Y = lambda z,t:Q(z, -5-t-2*z)
(y0,y4), (y5,y1), (y2,y6), (y7,y3) = (Y(z0,t0), Y(z1,t1), Y(z2,t0), Y(z3,t1)); y = [y0,y1,y2,y3,y4,y5,y6,y7];

X = lambda n:Q(y[n],t[n&1]+y[n]+y[(n+2)&7]+2*y[(n+5)&7]);
(x0,x8),(x1,x9),(x2,x10),(x3,x11), (x4,x12),(x5,x13),(x14,x6),(x7,x15) = map(X, range(8)); x = [x0,x1,x2,x3, x4,x5,x6,x7, x8,x9,x10,x11, x12,x13,x14,x15];

V = lambda n:Q(x[n], x[n]+x[(n+1)&15]+x[(n+2)&15]+x[(n+5)&15]);
(v0,v6), (v1,v7), (v2,v8), (v3,v9), (v4,v10), (v5,v11) = map(V, [0,1,7,8,9,15]); v = [v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11];

(u0,u4), (u1,u5), (u2,u6), (u3,u7) = Q(v0, v1+v2), Q(v3, v4+v5), Q(v6,v7+v8), Q(v9, v10+v11); u = [u0,u1,u2,u3,u4,u5,u6,u7]
(w0,w4), (w1,w5), (w2,w6), (w3,w7) = Q(u0,u1), Q(u2,u3), Q(u4,u5), Q(u6,u7); w = [-w7,w0,w1,w2,w3,w4,w5,w6,w7]

S = lambda a:"[ " + " | ".join(map(lambda x:str(x), a)) + " ] ";
print( 'Here is how to calculate real radical form expression for %s -' % ('cos(pi*%s/257)'%[2**n for n in range(9)]).replace(' ','') )
print( "Calculate: t[2] => z[4] => y[8] => x[16] => v[12] => u[8] => w[9]" )
print( "t = %s\nz = %s\ny = %s\nx = %s\nv = %s\nu = %s\nw = %s"%(S(t),S(z),S(y),S(x),S(v),S(u),S(w)) )
#print( "t = %s\nz = %s\ny = %s\nx = %s\nv = %s\nu = %s\nw = %s"%tuple([S(m) for m in [t,z,y,x,v,u,w]]); )
print( '\n'.join(['%s = %-14s = %s'%('2*cos(%3s*pi/257)'%2**n,2*cos(pi/257*2**n),str(w[n])) for n in range(9)]) )

def paw(): # print( acos w/2  )
    print( 'paw() =', [ round(acos(float(z)/2)*257/pi,12) for z in w if abs(z)<=2 ] )

paw()
