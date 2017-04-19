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
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
from datetime import datetime

###
plt.close("all") #close all; </matlab>
#mlab.close(all=True)
###

def f(x):
    return 100*np.exp(-10*x)

def exact(x):
    return 1.0-(1-np.exp(-10))*x-np.exp(-10*x)

# Hardcoded params for simplicity
#fileout = pyOutput
exponent = 5
#n = 4
big_error_array = [] # overall error
n_arr = [] # array of n for plotting overall error
for i in range(1, exponent+1):
    current_i = i
    
    n = 10**i
 
    n_arr.append(n)
    
    # Append i to filename
    fileout = 'pyOutputSimple'
    fileout += str(i)
    
    # descretization
    h = 1/n
    hh = h*h
    
    d = np.zeros(n+1)
    b = np.zeros(n+1)
    x = np.zeros(n+1)
    solution = np.zeros(n+1)
    # Adding predetermined values to matrix
    d[0] = 2
    d[n] = 2
    solution[0] = 0
    solution[n] = 0
    
            #Starting Timer
    begintime = datetime.now()
            
    for i in range(1,n):
        d[i] = (i+1)/i
    for i in range(1,n+1):
        x[i] = i*h
        b[i] = hh*f(i*h)
    
    # FW sub
    for i in range(2,n):
        b[i] = b[i] + b[i-1]/d[i-1]
    # Backward sub
    solution[n-1] = b[n-1]/d[n-1]    
    for i in range((n-2),0,-1):
        solution[i] = (b[i]+solution[i+1])/d[i]
        
    print(datetime.now() - begintime)
    
    # Plot the results
#    plot_x_axis = np.linspace(0,1,len(solution))
    plt.figure()    
#    plt.plot(plot_x_axis, solution[:], label='Iterative')
#    plt.plot(plot_x_axis, exact(x[:]), label='Exact/analytical')
    plt.plot(solution[:], label='Iterative')
    plt.plot(exact(x[:]), label='Exact/analytical')
    current_exp = str(i)
    plb.title(r'n=$10^{}$'.format(current_i))
    plb.xlabel('x')
    plb.ylabel('u(x)')
    #plt.legend(bbox_to_anchor = (1.1,.8))
    # Put some useful grid lines
    plt.grid(b=True, which='major', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', linestyle='-', linewidth=0.1)    

    plt.legend()
    plt.show()
    # Save plot iteratively
    plt.savefig(str(current_i)+'.png')
    
 
    
#    with open(fileout, 'w') as fout:
#        fout.write('x:\t\tApprox:\t\tExact:\t\tRelative Error:\n')
    RelativeError_arr = []
    for j in range(1,n):
        RelativeError = np.abs((exact(x[j])-solution[j])/exact(x[j]))
        RelativeError_arr.append(RelativeError)
#        fout.writelines('{0:.8f}'.format(x[j]) + '\t')
#        fout.writelines('{0:.8f}'.format(solution[j]) + '\t')
#        fout.writelines('{0:.8f}'.format(exact(x[j])) + '\t')
#        fout.writelines('{0:.8f}'.format(np.log10(RelativeError)) + '\n')
##    fout.closed
   
#    print('File: ' + str(i) + '/' + str(exponent) + ' written.')
    #Plot relative error
    plt.figure()
    plt.plot(np.log10(RelativeError_arr))
    plb.title('Log of relative error for: ' + r'n=$10^{}$'.format(current_i))
    plb.xlabel('x')
    plb.ylabel('Relative Error (log)')
    # Put some useful grid lines
    plt.grid(b=True, which='major', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', linestyle='-', linewidth=0.1)    
    #plt.yscale('log')
    plt.show()
    plt.savefig(str(current_i)+'_error.png')
    
    # appendn average of error to big error array
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
# Put some useful grid lines
plt.grid(b=True, which='major', linestyle='-', linewidth=0.5)
plt.minorticks_on()
plt.grid(b=True, which='minor', linestyle='-', linewidth=0.1)    
plt.show()
plt.savefig('BigError_log.png')

