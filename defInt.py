#!/usr/bin/env python3 -i

# Numeric Method for Definite Integrals, f(x) = F'(x), F(b)-F(a) = Definite Integral = defInt(a, b, f)
# Example: Integrate Power Function f(x) = x^n, so F(x) = x^(n+1) / (n+1)

M, N = 7, 10

a, b = 1, 5
f = lambda x, n=N: x**n; F = lambda x,n=N: x**(n+1)/(n+1)
defInt = lambda a,b,f,m=10**M: (b-a)/m * (sum([f(a + (b-a)/m*k) for k in range(m+1)]) - (f(a)+f(b)/2))
print('Compare >>> defInt(a,b,f), F(b)-F(a)')
