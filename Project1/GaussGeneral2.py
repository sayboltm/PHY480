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

for k in range(1, exponent+1):
    # Weird thing we didn't understand
    n = 10**k
    
    # Append i to filename
    fileout = 'pyOutputSimple'
    fileout += str(k)
    
    # lol wut.. probs descretization of stuff
    h = 1/n
    hh = h*h
  
    ''''''
  
    d = np.zeros(n+1)
    b = np.zeros(n+1)
    x = np.zeros(n+1)
    solution = np.zeros(n+1)
    
    d[0] = 2
    d[n] = 2
    solution[0] = 0
    solution[n] = 0
    for i in range(1,n):
        d[i] = (i+1)/i
    for i in range(0,n+1):
        x[i] = i*h
        b[i] = hh*f(i*h)
    
    # FW sub
    for i in range(2,n):
        b[i] = b[i] + b[i-1]/d[i-1]
    # Backward sub
    solution[n-1] = b[n-1]/d[n-1]    
    for i in range((n-2),0,-1):
        solution[i] = (b[i]+solution[i+1])/d[i]
        
    with open(fileout, 'w') as fout:
        fout.write('x:\t\tApprox:\t\tExact:\t\tRelative Error:\n')
        for j in range(1,n):
            RelativeError = np.abs((exact(x[j])-solution[j])/exact(x[j]))
            fout.writelines('{0:.8f}'.format(x[j]) + '\t') 
            fout.writelines('{0:.8f}'.format(solution[j]) + '\t')# This is wrong
            fout.writelines('{0:.8f}'.format(exact(x[j])) + '\t')# This is right
            fout.writelines('{0:.8f}'.format(np.log10(RelativeError)) + '\n')# This is wrong but might be right
    fout.closed
    print('File: ' + str(k) + '/' + str(exponent) + ' written.')





'''
    ### New for v2:
    n = n-1
    
    # Declare new mat
    A = np.zeros((n,n))
    
    b = np.zeros(n)
    x = np.zeros(n)

    # Setup initial elements that don't fit pattern
    A[0,0] = 2
    A[0,1] = -1
     
    x[0] = h
    b[0] = hh*f(x[0])

    #for i in range(1,n-1):
    for ii in range(1,n-1):
        x[ii] = x[ii-1] + h
        b[ii] = hh*f(x[ii])
        A[ii, ii-1] = -1
        A[ii,ii] = 2
        A[ii, ii+1] = -1


    A[n-1,n-2] = -1
    A[n-1,n-1] = 2

    x[n-1] = x[0]+(n-1)*h
    b[n-1] = hh*f(x[n-1])


    
    # Solve Ax = b
    #solution = A2**(-1)*b
    #sol2 = np.linalg.inv(A)*b
    sol3  = np.dot(np.linalg.inv(A),b)
    solution = np.linalg.solve(A,b)
    
    print('sol3: ' + str(sol3))
    print('solution: ' + str(solution))    
'''
