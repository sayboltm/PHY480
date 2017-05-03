# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 12:38:40 2017
Project 3: Verlet: might not work
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

'''
    m*d^2x/dt^2 = F(x,t)
        # From example,
        Asun = -MGsun * r/norm(r)**3
        # Thus,
        dv_x/dt = -MGsun * x /r^3
        dv_y/dt = ..
        
    dx/dt = v(x,t)
    dv/dt = F(x,t)/m
    
    
    x_i+1 = x_i + h*v_i + h^2/2 * vi'
    v_i+1 = v_i + h/2*(v'_i+1 + v'_i)
    
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

    def __init__(self, name, x, y, z, vx, vy, vz, m, N):
        # General parameters 
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx*365 # muls 365 to convert units don't have to copy/paste
        self.vy = vy*365
        self.vz = vz*365
        self.m = m
        self.r = np.sqrt(x**2 + y**2)
        
        # Difference parameters, updated with diffPlanet
#        self.md = []  # should just mkae single value.. integrazte diffPlanet into this to use self as one param??
#        self.rd = []
#        self.xd = []
#        self.yd = []
        
        self.diff_index = [] # For storing the names in the same order as used later
        
        # Arrays to store/plot stuff at end
        self.x_arr = np.zeros(N)
        self.y_arr = np.zeros(N)
        self.vx_arr = np.zeros(N)
        self.vy_arr = np.zeros(N)
        self.r_arr = np.zeros(N)
        
    def genR(self):
        # Call this to actually update r with the new x and y
        self.r = np.sqrt(self.x**2 + self.y**2)
        
#    def whoami(self):
#        return type(self).__name__
        
#    def __repr__(self):
#        return str(self)

def diffPlanet(current, other):
    m_sun = 1.989e30

    md = other.m/m_sun
    xd = current.x - other.x
    yd = current.y - other.y
    rd = np.sqrt((current.x-other.x)**2 + (current.y-other.y)**2)

    return md, rd, xd, yd     
    
#M_sun = 2e30 # kg
#M_earth = 6e24



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
   
AU = 1.5e11
N = 15000 # mesh points

Mercury = Planet('Mercury', 8.968367955950400E-02, 2.992196150489325E-01,
                 1.599362695939906E-02, -3.263506651781252E-02,
                 8.994926847931269E-03, 3.728209609803519E-03, 3.285e23, N)

Venus = Planet('Venus', -7.157250830876660E-01, -5.463746561907697E-03,
               4.119492719005560E-02, 1.571327619572131E-04,
               -2.030702486642804E-02, -2.877803459876483E-04, 4.867e24, N)

Earth = Planet('Earth', -9.927202732475465E-01, -3.572900718985997E-02,
               -1.457459024144764E-04, 4.051841001203786E-04,
               -1.725183415131579E-02, 1.301878530083015E-06, 6e24, N)
   
Mars = Planet('Mars', 6.964271442280220E-01, 1.336186237410552E+00,
              1.074113383386008E-02, -1.188514840056006E-02,
              7.661099748032458E-03,  4.520818773004982E-04, 6.39e23, N)

Jupiter = Planet('Jupiter', -5.218545007266457E+00, -1.573296133029459E+00,
                 1.232426758421258E-01, 2.089612419969210E-03,
                 -6.867936621102540E-03, -1.826325534616215E-05, 1.898e27, N)

Saturn = Planet('Saturn', -1.444219825937719E+00, -9.941663023738931E+00,
                2.303359552729894E-01, 5.214363552028829E-03,
                -8.202877354316839E-04, -1.929777394638974E-04, 5.683e26, N)

Uranus = Planet('Uranus', 1.821297304478037E+01, 8.107332098409824E+00,
                -2.058417371481961E-01, -1.628389773951803E-03,
                3.409882688003075E-03, 3.384857367884728E-05, 8.681e25, N)

Neptune = Planet('Neptune', 2.841901110626624E+01, -9.447028517683961E+00,
                 -4.604010687768234E-01, 9.694142585199833E-04,
                 2.997924119743549E-03, -8.374103237166192E-05, 1.024e26, N)

Pluto = Planet('Pluto', 9.911780279031699E+00, -3.177666918637830E+01,
               5.332377813548366E-01, 3.072019865872833E-03,
               2.921185031268098E-04, -9.159655153717684E-04, 1.309e22, N)
               
PlanetX = Planet('PlanetX', 1,0,0,0,1,0,9000, N) # A test planet for screwing with classes



planet_list = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune,
               Pluto]
#planet_list = [Earth, Jupiter]
#planet_list = [Earth, Jupiter, PlanetX]
#planet_list = [Earth]

# Test looping and skipping
for planet in planet_list:
    # Works as expected
    print('Current planet: ', planet.name)
    for otherplanet in planet_list:
        if otherplanet == planet:
            continue
        print('\totherplanet: ', otherplanet.name)
        
ts = 0
te = 4*np.pi#10#4*np.pi
h = (te-ts)/float(N)

t_arr = np.zeros(N)

t = ts

# Setup some extra arrays in the planets
for planet in planet_list:
    #print('Current planet: ', planet.name)
#    for otherplanet in planet_list:
#        if otherplanet == planet:
#            continue
#        #print('\tSubplanet: ', otherplanet.name)
    planet.md = np.zeros(len(planet_list)-1)
    planet.rd = np.zeros(len(planet_list)-1)
    planet.xd = np.zeros(len(planet_list)-1) 
    planet.yd = np.zeros(len(planet_list)-1)
    planet.forcex = np.zeros(len(planet_list)-1)
    planet.forcey = np.zeros(len(planet_list)-1) # An additional force component since it needs to be summed as a whole in the velocity update
    for otherplanet in planet_list:
        if otherplanet == planet:
            continue
        planet.diff_index.append(otherplanet.name) # used to track order of planet iteration, contains planets in order they are printed here
        # i.e. Earth.diff_index contains [Jupiter, PlanetX], and Earth.dx contains [DistEarthJupiter, DistEarthPlanetX] ...
        
i = 0
#while (t < te):
for i in range(N): #moar reliable?    

    t_arr[i] = t
     
    # Apply ops for each planet
    for planet in planet_list:
        j = 0
        for otherplanet in planet_list:
            if otherplanet == planet:
                continue
            md, rd, xd, yd = diffPlanet(planet, otherplanet)
#            planet.md.append(md)
#            planet.rd.append(rd)
#            planet.xd.append(xd)
#            planet.yd.append(yd) # NOTE: Tis will grow as N increases, fix.
            #planet.md[planet_list.index(otherplanet)] = md
            planet.md[j] = md
            planet.rd[j] = rd
            planet.yd[j] = yd # coord differences last to easily add z
            planet.xd[j] = xd
           
            # dv_x/dt = -GMsun/r^3*x
            planet.forcex[j] = planet.md[j]*planet.xd[j]/planet.rd[j]**3
            planet.forcey[j] = planet.md[j]*planet.yd[j]/planet.rd[j]**3
            j =+ 1 # Need to index numerically for np arrays

            
            
        #planet.dm, planet.dr, planet.dx, planet.dy = diffPlanet(planet, )

#    xe_arr[i] = x
#    ye_arr[i] = y
#    vxe_arr[i] = vx
#    vye_arr[i] = vy

#    mde, rde, xde, yde = diffPlanet(Earth, Jupiter)    
#    mdj, rdj, xdj, ydj = diffPlanet(Jupiter, Earth)    
    
    # instead of doing thsi shit separately earth, xy genR, jupiter xy genR,
    # do for planet in the planetlist
    for planet in planet_list: 
        # TODO: Cannot updatae position and velocity at same time
        ''' Must break up and do two for planet in planetlist, first updating 
        position, storing old acceleration, then updating velocity,
        recalculating acceleration as well as using the stored old value '''
        
        ''' Eventually need to move into planet.pos[0,1] instead of planet.x, 
        planet.y '''
    
        planet.x_arr[i] = planet.x # Store current values to array to plot later
        planet.y_arr[i] = planet.y
        planet.vx_arr[i] = planet.vx
        planet.vy_arr[i] = planet.vy
    
        #x_old = planet.x
        x_acceleration_old = np.sum(planet.forcex)/planet.m
        #planet.x = planet.x + h*planet.vx # Euler pos update
        planet.x = planet.x + h*planet.vx + h**2/2*(np.sum(planet.forcex)/planet.m) # Verlet pos update
        #planet.vx = planet.vx - h*4*np.pi**2*(x_old/planet.r**3 + np.sum(planet.forcex))
        planet.vx = planet.vx + h/2((x_acceleration_old) + ())
        
        
        y_old = planet.y
        planet.y = planet.y + h*planet.vy
        planet.vy = planet.vy - h*4*np.pi**2*(y_old/planet.r**3 + np.sum(planet.forcey))
        
        planet.genR() # This will update earth.r with the new r from new x and y    
    
    t += h
    i += 1
    
#Plottr.plot(xe_arr, ye_arr)
#Plottr.plot(Earth.x_arr, Earth.y_arr)
#Plottr.plot(Jupiter.x_arr, Jupiter.y_arr)
for planet in planet_list:
    Plottr.plot(planet.x_arr, planet.y_arr, 'xpos', 'ypos', planet.name + ' Trajectory')

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
   
   
   
Potentially useful links:
https://www.google.com/webhp?sourceid=chrome-instant&rlz=1C1ASUC_enUS657US657&ion=1&espv=2&ie=UTF-8#q=velocity+verlet+python
http://codepad.org/FcbFcoue
http://gdrcorelec.ups-tlse.fr/files/python_verlet.pdf
http://stackoverflow.com/questions/29009771/verlet-algorithm-implementation-in-python

'''
