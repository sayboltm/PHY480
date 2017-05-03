#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 15:32:46 2017

@author: Morten

see 'ode-print.pdf'
"""
#### clear;
from IPython import get_ipython
get_ipython().magic('reset -sf')
#####

#
# This program solves Newtons equation for a block sliding on
# an horizontal frictionless surface. i.e. bouncing off a wall on a spring

# F = -k*x, where k is sprg constant, x is position

# The block is tied to the wall with a spring, so N’s eq takes the form:
#   
#  m d^2x/dt^2 = - kx
#
# with k the spring tension and m the mass of block

# alternatively,

# d^2x/dt^2 = -k/m*x = -w0^2*x

# The angular frequency is omega**2 = k/m and we set it equal to 1 here

# The analytical solutions will have form: 
#  x(t) = Acos(w0*t + phi), where A is amplitude, and phi is phase constant

# In order to make the solution dimless, we set k/m = 1.
# This results in two coupled diff. eq’s (on for pos x and one for velocity v
# that may be written as:
#  dx(t)/dt = v(t)
#  dv(t)/dt = -w0^2*x(t)
#or
#  dx/dt = v
#  dv/dt = -x

# The user has to specify the initial velocity and position,
# and the number of steps. The time interval is fixed to
# t \in [0, 4\pi) (two periods)
# Note that this is a highly simplifyed rk4 code, intended
# for conceptual understanding and experimentation.:
    
import sys
import math
import numpy as np

import matplotlib.pyplot as plt
#import matplotlib.pylab as plb

#sys.path.append('C:\\Users\\Mike\\Dropbox\\Documents\\Programming\\Python\\ClassDev')
sys.path.append('C:\\Users\\Mike\\Documents\\GitHub\\sayboltm\\PHY480\\')
import Plottr

###
plt.close("all") #close all; </matlab>
#mlab.close(all=True)
###

#Global variables
ofile = None;
E0 = 0.0

def sim(x_0, v_0, N):
    ts = 0.0 # Time start
    te = 4*math.pi # Time end
    h = (te-ts)/float(N) # Discretize timespace, create time step
    
    t_arr = np.zeros(N)
    x_arr = np.zeros(N)
    v_arr = np.zeros(N)
    de_arr = np.zeros(N)

    # set current time t = tstart, current x = x_0, v = v_0
    t = ts; 
    x = x_0
    v = v_0
    
    i=0
    while (t < te):
        ''' Runge-Kutta 4 solve: (see ode-print.pdf ~p9, ~p14, p20)
        Have 2 DE, so need k1, k2, k3, and k4
        k1 = h*f(ti,yi), k2 = h*f(ti+h/2, yi+k1/2)
        k3 = h*f(ti+h/2, yi+k2/2), k4 = h*f(ti+h, yi+k3)
        
        y_i+1 = yi + 1/6*(k1 + 2*k2 + 2*k3 + k4)
        
        For this problem, velocityf(t,y) = -x, and positionf(t,y) = v
        because:
        dx(t)/dt = v(t), or dx/dt = v
        dv(t)/dt = -w0^2*x(t), or dv/dt = -x, since w0 is normalized to 1
        
        so 2 DEs so need 2 of each coefficient and final next solution (yi+1)
        '''
        
        kv1 = -h*x
        kx1 = h*v
        kv2 = -h*(x+kx1/2)
        kx2 = h*(v+kv1/2)
        kv3 = -h*(x+kx2/2)
        kx3 = h*(v+kv2/2)
        kv4 = -h*(x+kx3/2)
        kx4 = h*(v+kv3/2)
        
        #Write the old values to file, save de result to array
        de_arr[i] = output(t,x,v)
        # Also save to array for plotting
#        t_lst.append(t)
#        x_lst.append(x)
#        v_lst.append(v)
        t_arr[i] = t # save other vars in addition to printing to file
        x_arr[i] = x
        v_arr[i] = v
        
        #Update
        x = x + (kx1 + 2*(kx2+kx3) + kx4)/6
        v = v + (kv1 + 2*(kv2+kv3) + kv4)/6
        
        t += h # new time = time + step
        i += 1
    
    #plot some stuff
    Plottr.plot(t_arr, x_arr, 'time', 'position', 'Position plot')
    Plottr.plot(t_arr, v_arr, 'time', 'velocity', 'Velocity plot')
    Plottr.plot(t_arr, de_arr, 'time', 'wut', 'DE plot')

def output(t,x,v):
    # modified to return de for saving/processing
    de = 0.5*x**2+0.5*v**2 - E0;
    ofile.write("%15.8E %15.8E %15.8E %15.8E %15.8E\n"\
                %(t, x, v, math.cos(t),de));
    return de

                
#MAIN PROGRAM:
#Get input
if len(sys.argv) == 5: # progname.py fileout initPos initVel N
    ofilename = sys.argv[1]; 

    x_0 = float(sys.argv[2])
    v_0 = float(sys.argv[3])
    N = int(sys.argv[4]) # This is the number of differential equations (use N=2?) no resolution unlike C++ file
else:
#    print ("Usage:", sys.argv[0], "ofilename x0 v0 N")
#    sys.exit(0)

    # For debugging, jumps here then given these inputs instead of via cmd line
    ofilename = 'testfile.txt'
    x_0 = 1 # initial position
    v_0 = 0 # initial velocity
    N = 97 # Number of mesh points
    # why TAF is 97 the highest number in bounds????
    # this is because t is slightly less than te for longer with higher numbers
    # so the while loop goes through an extra time creating out of bounds
    # why?????f

#Setup
ofile = open(ofilename, 'w')
E0 = 0.5*x_0**2+0.5*v_0**2

# Print a header line to the file:
ofile.write('t\t\t x\t\t v\t\t cos(t)\t\t de\n')

#Run simulation
sim(x_0,v_0,N)

#Cleanup
ofile.close()