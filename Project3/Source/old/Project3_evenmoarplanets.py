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

    def __init__(self, x, y, z, vx, vy, vz, m):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx*365 # muls 365 to convert units don't have to copy/paste
        self.vy = vy*365
        self.vz = vz*365
        self.m = m
        self.r = np.sqrt(x**2 + y**2)
        
        self.x_arr = np.zeros(N) # Somehow N is passed to these.............
        self.y_arr = np.zeros(N)
        self.vx_arr = np.zeros(N)
        self.vy_arr = np.zeros(N)
        self.r_arr = np.zeros(N)
        
    def genR(self):
        # Call this to actually update r with the new x and y
        self.r = np.sqrt(self.x**2 + self.y**2)

def diffPlanet(current, other):
    m_sun = 1.989e30

    md = other.m/m_sun
    xd = current.x - other.x
    yd = current.y - other.y
    rd = np.sqrt((current.x-other.x)**2 + (current.y-other.y)**2)

    return md, rd, xd, yd     
    
#M_sun = 2e30 # kg
#M_earth = 6e24

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

Mercury = Planet(8.968367955950400E-02, 2.992196150489325E-01,
                 1.599362695939906E-02, -3.263506651781252E-02,
                 8.994926847931269E-03, 3.728209609803519E-03, 3.285e23)

Venus = Planet(-7.157250830876660E-01, -5.463746561907697E-03,
               4.119492719005560E-02, 1.571327619572131E-04,
               -2.030702486642804E-02, -2.877803459876483E-04, 4.867e24)

Earth = Planet(-9.927202732475465E-01, -3.572900718985997E-02,
               -1.457459024144764E-04, 4.051841001203786E-04,
               -1.725183415131579E-02, 1.301878530083015E-06, 6e24)
   
Mars = Planet(6.964271442280220E-01, 1.336186237410552E+00,
              1.074113383386008E-02, -1.188514840056006E-02,
              7.661099748032458E-03,  4.520818773004982E-04, 6.39e23)

Jupiter = Planet(-5.218545007266457E+00, -1.573296133029459E+00,
                 1.232426758421258E-01, 2.089612419969210E-03,
                 -6.867936621102540E-03, -1.826325534616215E-05, 1.898e27)

Saturn = Planet(-1.444219825937719E+00, -9.941663023738931E+00,
                2.303359552729894E-01, 5.214363552028829E-03,
                -8.202877354316839E-04, -1.929777394638974E-04, 5.683e26)

Uranus = Planet(1.821297304478037E+01, 8.107332098409824E+00,
                -2.058417371481961E-01, -1.628389773951803E-03,
                3.409882688003075E-03, 3.384857367884728E-05, 8.681e25)

Neptune = Planet(2.841901110626624E+01, -9.447028517683961E+00,
                 -4.604010687768234E-01, 9.694142585199833E-04,
                 2.997924119743549E-03, -8.374103237166192E-05, 1.024e26)

Pluto = Planet(9.911780279031699E+00, -3.177666918637830E+01,
               5.332377813548366E-01, 3.072019865872833E-03,
               2.921185031268098E-04, -9.159655153717684E-04, 1.309e22)
               
#planet_list = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune,
#               Pluto]
planet_list = [Earth]
      
#planetx = Planet(1,2,3,4,9000)         
#x_0_earth = -9.929762531318524E-01 #/ AU
#y_0_earth = -1.847273743153964E-02 #/ AU
##x_0_earth = 1 # AU
##y_0_earth = 0
#r_0_earth = np.sqrt(x_0_earth**2 + y_0_earth**2)
#vx_0_earth = 1.067738377436134E-04*365 #/ AU # units of AU/day
#vy_0_earth = -1.725983083065230E-02*365 #/ AU



ts = 0
te = 10#4*np.pi
h = (te-ts)/float(N)

t_arr = np.zeros(N)
#xe_arr = np.zeros(N)
#ye_arr = np.zeros(N)
#r_arr = np.zeros(N)
#vxe_arr = np.zeros(N)
#vye_arr = np.zeros(N)


t = ts
#x = earth.x#x_0_earth
#y = earth.y#y_0_earth
#r = earth.r#np.sqrt(x**2 + y**2)
#vx = earth.vx#vx_0_earth
#vy = earth.vy#vy_0_earth

i = 0
#while (t < te):
for i in range(N): #moar reliable?    
    t_arr[i] = t
#    xe_arr[i] = x
#    ye_arr[i] = y
#    vxe_arr[i] = vx
#    vye_arr[i] = vy

    mde, rde, xde, yde = diffPlanet(Earth, Jupiter)    
    mdj, rdj, xdj, ydj = diffPlanet(Jupiter, Earth)    
    
    
    Earth.x_arr[i] = Earth.x
    Earth.y_arr[i] = Earth.y
    Earth.vx_arr[i] = Earth.vx
    Earth.vy_arr[i] = Earth.vy
    
    # update
    # TODO: Why does the C++ Code ode-print p23 not save old value?? bc wrong. yay found a bug
    # TODO: Why is there no gravity?? Not enough timeto see (it is actually integrated in there)
    x_old = Earth.x
    Earth.x = Earth.x + h*Earth.vx
    #Earth.vx = Earth.vx - h*(4*np.pi**2/Earth.r**3)*x_old
    #vx = vx - h*(4*np.pi**2/r**3)*x
    Earth.vx = Earth.vx - h*4*np.pi**2*(x_old/Earth.r**3 + mde*xde/rde**3)
    
    y_old = Earth.y
    Earth.y = Earth.y + h*Earth.vy
    #Earth.vy = Earth.vy - h*(4*np.pi**2/Earth.r**3)*y_old
    #vy = vy - h*(4*np.pi**2/r**3)*y
    Earth.vy = Earth.vy - h*4*np.pi**2*(y_old/Earth.r**3 + mde*yde/rde**3)
    
    #r = np.sqrt(x**2 + y**2)
    Earth.genR() # This will update earth.r with the new r from new x and y
    
    
    Jupiter.x_arr[i] = Jupiter.x
    Jupiter.y_arr[i] = Jupiter.y
    Jupiter.vx_arr[i] = Jupiter.vx
    Jupiter.vy_arr[i] = Jupiter.vy
    
    x_old = Jupiter.x
    Jupiter.x = Jupiter.x + h*Jupiter.vx
    Jupiter.vx = Jupiter.vx - h*4*np.pi**2*(x_old/Jupiter.r**3 + mdj*xdj/rdj**3)
    #vx = vx - h*(4*np.pi**2/r**3)*x
    
    y_old = Jupiter.y
    Jupiter.y = Jupiter.y + h*Jupiter.vy
    Jupiter.vy = Jupiter.vy - h*4*np.pi**2*(y_old/Jupiter.r**3 + mdj*ydj/rdj**3)
    #vy = vy - h*(4*np.pi**2/r**3)*y
    
    Jupiter.genR() # This will update earth.r with the new r from new x and y
    
    
    t += h
    i += 1
    
#Plottr.plot(xe_arr, ye_arr)
Plottr.plot(Earth.x_arr, Earth.y_arr)
Plottr.plot(Jupiter.x_arr, Jupiter.y_arr)

'''
Planets:
MERCURY
*******************************************************************************
Ephemeris / WWW_USER Fri Mar 24 12:32:04 2017 Pasadena, USA      / Horizons    
*******************************************************************************
Target body name: Mercury (199)                   {source: DE431mx}
Center body name: Solar System Barycenter (0)     {source: DE431mx}
Center-site name: BODY CENTER
*******************************************************************************
Start time      : A.D. 2017-Mar-23 00:00:00.0000 TDB
Stop  time      : A.D. 2017-Apr-22 00:00:00.0000 TDB
Step-size       : 1440 minutes
*******************************************************************************
Center geodetic : 0.00000000,0.00000000,0.0000000 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 0.00000000,0.00000000,0.0000000 {E-lon(deg),Dxy(km),Dz(km)}
Center radii    : (undefined)                                                  
Output units    : AU-D                                                         
Output type     : GEOMETRIC cartesian states
Output format   : 3 (position, velocity, LT, range, range-rate)
Reference frame : ICRF/J2000.0                                                 
Coordinate systm: Ecliptic and Mean Equinox of Reference Epoch                 
*******************************************************************************
JDTDB
   X     Y     Z
   VX    VY    VZ
   LT    RG    RR
*******************************************************************************
$$SOE
2457835.500000000 = A.D. 2017-Mar-23 00:00:00.0000 TDB 
   8.968367955950400E-02  2.992196150489325E-01  1.599362695939906E-02
  -3.263506651781252E-02  8.994926847931269E-03  3.728209609803519E-03
   1.806466698607638E-03  3.127800129686671E-01 -5.618859842149030E-04
   
   
VENUS
2457835.500000000 = A.D. 2017-Mar-23 00:00:00.0000 TDB 
  -7.157250830876660E-01 -5.463746561907697E-03  4.119492719005560E-02
   1.571327619572131E-04 -2.030702486642804E-02 -2.877803459876483E-04
   4.140644952217086E-03  7.169304492860747E-01 -1.864408496542609E-05
   

EARTH
2457835.500000000 = A.D. 2017-Mar-23 00:00:00.0000 TDB 
  -9.927202732475465E-01 -3.572900718985997E-02 -1.457459024144764E-04
   4.051841001203786E-04 -1.725183415131579E-02  1.301878530083015E-06
   5.737186432394155E-03  9.933630374205216E-01  2.155870895460446E-04
   
MARS
2457835.500000000 = A.D. 2017-Mar-23 00:00:00.0000 TDB 
   6.964271442280220E-01  1.336186237410552E+00  1.074113383386008E-02
  -1.188514840056006E-02  7.661099748032458E-03  4.520818773004982E-04
   8.702691997702615E-03  1.506824409219270E+00  1.303650211233222E-03
   
JUPITER
2457835.500000000 = A.D. 2017-Mar-23 00:00:00.0000 TDB 
  -5.218545007266457E+00 -1.573296133029459E+00  1.232426758421258E-01
   2.089612419969210E-03 -6.867936621102540E-03 -1.826325534616215E-05
   3.148778561366333E-02  5.451941073802967E+00 -1.865191581533015E-05
   
SATURN
2457835.500000000 = A.D. 2017-Mar-23 00:00:00.0000 TDB 
  -1.444219825937719E+00 -9.941663023738931E+00  2.303359552729894E-01
   5.214363552028829E-03 -8.202877354316839E-04 -1.929777394638974E-04
   5.803619745996548E-02  1.004865609101540E+01  5.770794715855591E-05
   
URANUS
2457835.500000000 = A.D. 2017-Mar-23 00:00:00.0000 TDB 
   1.821297304478037E+01  8.107332098409824E+00 -2.058417371481961E-01
  -1.628389773951803E-03  3.409882688003075E-03  3.384857367884728E-05
   1.151464543247828E-01  1.993699053780572E+01 -1.013059185887147E-04
   
NEPTUNE
2457835.500000000 = A.D. 2017-Mar-23 00:00:00.0000 TDB 
   2.841901110626624E+01 -9.447028517683961E+00 -4.604010687768234E-01
   9.694142585199833E-04  2.997924119743549E-03 -8.374103237166192E-05
   1.729860309238847E-01  2.995160278209080E+01 -2.447700772967000E-05  
   
PLUTO
2457835.500000000 = A.D. 2017-Mar-23 00:00:00.0000 TDB 
   9.911780279031699E+00 -3.177666918637830E+01  5.332377813548366E-01
   3.072019865872833E-03  2.921185031268098E-04 -9.159655153717684E-04
   1.922722390104317E-01  3.329090619691495E+01  6.211367556276724E-04
'''