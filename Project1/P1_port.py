#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:16:55 2017
LU Decomp
@author: Mike
"""
#### clear;
from IPython import get_ipython
get_ipython().magic('reset -sf')
#####


import numpy as np


def f(x):
    return 100*np.exp(-10*x)

def exact(x):
    return 1.0-(1-np.exp(-10))*x-np.exp(-10*x)

# Hardcoded params for simplicity
#fileout = pyOutput
exponent = 4
#n = 4

for i in range(1, exponent):
    # Weird thing we didn't understand
    n = 10**i

    # Declare new mat
    A = np.zeros((n,n))
    
    # Append i to filename
    fileout = 'pyOutput'
    fileout += str(i)

    # Setup elements that don't fit pattern
    A[0,0] = 2
    A[0,1] = -1

    A[n-1,n-2] = -1
    A[n-1,n-1] = 2

    # lol wut.. probs descretization of stuff
    h = 1/n
    hh = h*h

    b = np.zeros(n)
    x = np.zeros(n)

    x[0] = h
    b[0] = hh*f(x[0])
    x[n-1] = x[0]+(n-1)*h
    b[n-1] = hh*f(x[n-1])

    #for i in range(1,n-1):
    for ii in range(1,n-1):
        x[ii] = x[ii-1] + h
        b[ii] = hh*f(x[ii])
        A[ii, ii-1] = -1
        A[ii,ii] = 2
        A[ii, ii+1] = -1
    
    # Solve Ax = b
    #solution = A2**(-1)*b
    #sol2 = np.linalg.inv(A)*b
    sol3  = np.dot(np.linalg.inv(A),b)
    solution = np.linalg.solve(A,b)
    
    print('sol3: ' + str(sol3))
    print('solution: ' + str(solution))    
    
    with open(fileout, 'w') as fout:
        for j in range(0,n):
            RelativeError = np.abs((exact(x[j])-solution[j])/exact(x[j]))
            fout.writelines(str(x[j]) + '\t')
            fout.writelines(str(solution[j]) + '\t')
            fout.writelines(str(exact(x[j])) + '\t')
            fout.writelines(str(np.log10(RelativeError)) + '\n')
    fout.closed
    print('File: ' + str(i) + '/' + str(exponent) + ' written.')






