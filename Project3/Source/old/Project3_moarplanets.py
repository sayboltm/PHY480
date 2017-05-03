# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 12:38:40 2017
Project 3 binary system test
@author: Mike
"""

''' The Earth-Sun system can be modeled by 4 coupled DEs: ODEp12
    v_x,i+1 = v_x,i - h*(4*pi^2/r^3_i)*x_i
    x_i+1 = x_i + h*v_x,i
    v_y,i+1 = v_y,i - h*(4*pi^2/r^3_i)*y_i
    y_i+1 = y_i + h*v_y,i
    
    # Kidding use these for RK4
    dv_x/dt = -GMsun/r^3*x
    dx/dt = v_x
    
    dv_y/dt = -GMsun/r^3*y
    dy/dt = v_y
    '''

#### clear;
from IPython import get_ipython
get_ipython().magic('reset -sf')
#####

import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.constants import G

sys.path.append('C:\\Users\\Mike\\Documents\\GitHub\\sayboltm\\PHY480\\')
import Plottr

###
plt.close("all") #close all; </matlab>
#mlab.close(all=True)
###


class Planet:
    ''' Planet class '''
    m_sun = 1.989e30 # kg

    def __init__(self, x, y, vx, vy, m, N):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m
        self.r = np.sqrt(x**2 + y**2)
        
        self.x_arr = np.zeros(N)
        self.y_arr = np.zeros(N)
        self.vx_arr = np.zeros(N)
        self.vy_arr = np.zeros(N)
        self.r_arr = np.zeros(N)
        
    def genR(self):
        # Call this to actually update r with the new x and y
        self.r = np.sqrt(self.x**2 + self.y**2)
        
M_sun = 2e30 # kg
M_earth = 6e24

AU = 1.5e11

N = 1500 # mesh points

''' Earth today:
JDTDB
   X     Y     Z
   VX    VY    VZ
   LT    RG    RR
*******************************************************************************
$$SOE
2457834.500000000 = A.D. 2017-Mar-22 00:00:00.0000 TDB 
  -9.929762531318524E-01 -1.847273743153964E-02 -1.470030806492116E-04
   1.067738377436134E-04 -1.725983083065230E-02  1.208887940688408E-06
   5.735944924757437E-03  9.931480770367996E-01  2.142804934355568E-04
   
   '''
earth = Planet(-9.929762531318524E-01, -1.847273743153964E-02,
               1.067738377436134E-04*365, -1.725983083065230E-02*365, 6e24, N)
      
planetx = Planet(1,2,3,4,9000,N)         
#x_0_earth = -9.929762531318524E-01 #/ AU
#y_0_earth = -1.847273743153964E-02 #/ AU
##x_0_earth = 1 # AU
##y_0_earth = 0
#r_0_earth = np.sqrt(x_0_earth**2 + y_0_earth**2)
#vx_0_earth = 1.067738377436134E-04*365 #/ AU # units of AU/day
#vy_0_earth = -1.725983083065230E-02*365 #/ AU



ts = 0
te = 1#4*np.pi
h = (te-ts)/float(N)

t_arr = np.zeros(N)
#xe_arr = np.zeros(N)
#ye_arr = np.zeros(N)
#r_arr = np.zeros(N)
#vxe_arr = np.zeros(N)
#vye_arr = np.zeros(N)


t = ts
x = earth.x#x_0_earth
y = earth.y#y_0_earth
r = earth.r#np.sqrt(x**2 + y**2)
vx = earth.vx#vx_0_earth
vy = earth.vy#vy_0_earth

i = 0
while (t < te):
    
    t_arr[i] = t
#    xe_arr[i] = x
#    ye_arr[i] = y
#    vxe_arr[i] = vx
#    vye_arr[i] = vy
    earth.x_arr[i] = earth.x
    earth.y_arr[i] = earth.y
    earth.vx_arr[i] = earth.vx
    earth.vy_arr[i] = earth.vy
    
    # update
    # TODO: Why does the C++ Code ode-print p23 not save old value?? bc wrong. yay found a bug
    # TODO: Why is there no gravity?? Not enough timeto see (it is actually integrated in there)
    x_old = earth.x
    earth.x = earth.x + h*earth.vx
    earth.vx = earth.vx - h*(4*np.pi**2/earth.r**3)*x_old
    #vx = vx - h*(4*np.pi**2/r**3)*x
    
    y_old = earth.y
    earth.y = earth.y + h*earth.vy
    earth.vy = earth.vy - h*(4*np.pi**2/earth.r**3)*y_old
    #vy = vy - h*(4*np.pi**2/r**3)*y
    
    #r = np.sqrt(x**2 + y**2)
    earth.genR() # This will update earth.r with the new r from new x and y
    
    t += h
    i += 1
    
#Plottr.plot(xe_arr, ye_arr)
Plottr.plot(earth.x_arr, earth.y_arr)