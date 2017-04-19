#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:16:55 2017
LU Decomp
@author: Mike
"""
#### clear;
#from IPython import get_ipython
#get_ipython().magic('reset -sf')
#####


import numpy as np


def f(x):
    return 100*np.exp(-10*x)

def exact(x):
    return 1.0-(1-np.exp(-10))*x-exp(-10*x)	
    
n = 5

A = np.zeros((n,n))

A[0,0] = 2
A[0,1] = -1

A[n-1,n-2] = -1
A[n-1,n-1] = 2

h = 1/n
hh = h*h

b = np.zeros(n)
x = np.zeros(n)

x[0] = h
b[0] = hh*f(x[0])
x[n-1] = x[0]+(n-1)*h
b[n-1] = hh*f(x[n-1])

for i in range(1,n-1):
    x[i] = x[i-1] + h
    b[i] = hh*f(x[i])
    A[i, i-1] = -1
    A[i,i] = 2
    A[i, i+1] = -1
    
# Solve Ax = b
#solution = A2**(-1)*b
#sol2 = np.linalg.inv(A)*b
sol3 = np.dot(np.linalg.inv(A),b)
solution = np.linalg.solve(A,b)
    
print('sol3: ' + str(sol3))
print('solution: ' + str(solution))    
    
