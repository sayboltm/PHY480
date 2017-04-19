#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:16:55 2017
LU Decomp
NOTE: This is not the implementation of LU decomp algo 
@author: Mike
"""
#### clear;
from IPython import get_ipython
get_ipython().magic('reset -sf')
#####


import numpy as np
import matplotlib.pyplot as plt
#import plottr.py as Plottr
import matplotlib.pylab as plb
from datetime import datetime

def f(x):
    return 100*np.exp(-10*x)

def exact(x):
    return 1.0-(1-np.exp(-10))*x-np.exp(-10*x)

# Hardcoded params for simplicity
#fileout = pyOutput
#expoent=4
exponent = 5
#n = 4

# List of error averages for each n
big_error_array = []
n_arr = []
for i in range(1, exponent):
    n = 10**i
    n_arr.append(n)
    
    steps = n/10
    
    # Append i to filename
    fileout = 'pyOutput'
    fileout += str(i)
    
    # lDescretization
    h = 1/n
    hh = h*h
    
    # Study points between endpoints
    n = n-1
    
    # Declare new mats
    A = np.zeros((n,n))
    
    b = np.zeros(n)
    x = np.zeros(n)

    # Setup initial elements that don't fit rest of tridiagonal pattern
    A[0,0] = 2
    A[0,1] = -1
     
    x[0] = h
    b[0] = hh*f(x[0])

    #Starting Timer
    begintime = datetime.now()
    
    # Build tridiagonal matrix
    #for i in range(1,n-1):
    for ii in range(1,n-1):
        x[ii] = x[ii-1] + h
        b[ii] = hh*f(x[ii])
        A[ii, ii-1] = -1
        A[ii,ii] = 2
        A[ii, ii+1] = -1
        # Attempt at progress bar
        #print("\r{0}".format((float(i)/n)*100),)
        #sys.stdout.flush()
        
        # Print progress at every 10%
        if ii%steps==0:
            print(str(ii) + '/' + str(n) + '\n')

    # set up end elemnts that don't fit pattern
    A[n-1,n-2] = -1
    A[n-1,n-1] = 2

    x[n-1] = x[0]+(n-1)*h
    b[n-1] = hh*f(x[n-1])


    
    #Solve Ax = b
#    solution = A2**(-1)*b
#    sol2 = np.linalg.inv(A)*b
#    sol3  = np.dot(np.linalg.inv(A),b)
    solution = np.linalg.solve(A,b)
    print(datetime.now() - begintime)
    
#    print('sol3: ' + str(sol3))
    print('solution: ' + str(solution))   
    
    # Plot the results
#    plot_x_axis = np.linspace(0,1,len(solution))
    plt.figure()    
#    plt.plot(plot_x_axis, solution[:], label='Iterative')
#    plt.plot(plot_x_axis, exact(x[:]), label='Exact/analytical')
    plt.plot(solution[:], label='Iterative')
    plt.plot(exact(x[:]), label='Exact/analytical')
    
    # Put current exponent such that shows up inside LaTeX string
    current_exp = str(i)
    plb.title(r'n=$10^{}$'.format(i))
    
    plb.xlabel('x')
    plb.ylabel('u(x)')
    # Put some useful grid lines
    plt.grid(b=True, which='major', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', linestyle='-', linewidth=0.1)    
    plt.legend()
    plt.show()
    # Save plot iteratively
    plt.savefig(str(i)+'.png')
    
    RelativeError_arr = []
    for j in range(1,n):
        RelativeError = np.abs((exact(x[j])-solution[j])/exact(x[j]))
        RelativeError_arr.append(RelativeError)
  
#    with open(fileout, 'w') as fout:
#        fout.write('x:\t\tApprox:\t\tExact:\t\tRelative Error:\n')
#        for j in range(0,n):
#            RelativeError = np.abs((exact(x[j])-solution[j])/exact(x[j]))
#            fout.writelines('{0:.8f}'.format(x[j]) + '\t')
#            fout.writelines('{0:.8f}'.format(solution[j]) + '\t')
#            fout.writelines('{0:.8f}'.format(exact(x[j])) + '\t')
#            fout.writelines('{0:.8f}'.format(np.log10(RelativeError)) + '\n')
#    fout.closed
#    print('File: ' + str(i) + '/' + str(exponent) + ' written.')
#    
    #Plot relative error
    plt.figure()
    plt.plot(np.log10(RelativeError_arr))
    plb.title('Log of relative error for: ' + r'n=$10^{}$'.format(i))
    plb.xlabel('x')
    plb.ylabel('Relative Error (log)')
    # Put some useful grid lines
    plt.grid(b=True, which='major', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', linestyle='-', linewidth=0.1)    
    #plt.yscale('log')
    plt.show()
    plt.savefig(str(i)+'_error.png')
    
    # append average of error to big error array
    big_error_array.append(np.average(RelativeError_arr[:]))
    
    

plt.figure()
plt.plot(n_arr, big_error_array)
plb.title('Average Error With Respect to n')
plb.xlabel('n')
plb.ylabel('Relative Error')
#plt.yscale('log')
# Put some useful grid lines
plt.grid(b=True, which='major', linestyle='-', linewidth=0.5)
plt.minorticks_on()
plt.grid(b=True, which='minor', linestyle='-', linewidth=0.1)    
plt.show()
plt.savefig('BigError.png')

plt.figure()
plt.plot(n_arr, big_error_array)
plb.title('Average Error With Respect to n')
plb.xlabel('n')
plb.ylabel('Relative Error')
plt.yscale('log')
plt.xscale('log')
# Put some useful grid lines
plt.grid(b=True, which='major', linestyle='-', linewidth=0.5)
plt.minorticks_on()
plt.grid(b=True, which='minor', linestyle='-', linewidth=0.1)    
plt.show()
plt.savefig('BigError_log.png')

