# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 12:38:40 2017
Project 3 binary system test

@author: Mike
"""
# TODO: Fix. Planets go in a straight trajectory

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

#sys.path.append('C:\\Users\\Mike\\Documents\\GitHub\\sayboltm\\PHY480\\')
#sys.path.append('~/GitHub/sayboltm/PHY480')
sys.path.append('/home/mike/GitHub/sayboltm/PHY480')
import Plottr

###
plt.close("all") #close all; </matlab>
#mlab.close(all=True)
###

from solar_system import *

AU = 1.5e11
N = 15000 # mesh points

#planet_list = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune,
#               Pluto]
#planet_list = [Mercury, Earth, Mars, Jupiter] # shorter list for debugging
#planet_list = [Earth, Jupiter]
#planet_list = [Earth, Jupiter, PlanetX]
planet_list = [Earth]

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
    
    # Experimental: go back and add arrays because don't want N in other file
    planet.x_arr = np.zeros(N)
    planet.y_arr = np.zeros(N)
    planet.vx_arr = np.zeros(N)
    planet.vy_arr = np.zeros(N)
    planet.r_arr = np.zeros(N)
    
    # Need variable to store old acceleration
    planet.x_acc_old = None
    planet.y_acc_old = None
    
def refreshPlanets(planet_list):
    for planet in planet_list:
        j = 0
        for otherplanet in planet_list:
            if otherplanet == planet:
                continue
            # diffPlanet depends on position only, not velocity
            md, rd, xd, yd = planet.diffPlanet(planet, otherplanet)
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
    
i = 0
#while (t < te):
for i in range(N): #moar reliable?    

    t_arr[i] = t
     
    # Apply ops for each planet
#    for planet in planet_list:
#        j = 0
#        for otherplanet in planet_list:
#            if otherplanet == planet:
#                continue
#            # diffPlanet depends on position only, not velocity
#            md, rd, xd, yd = planet.diffPlanet(planet, otherplanet)
##            planet.md.append(md)
##            planet.rd.append(rd)
##            planet.xd.append(xd)
##            planet.yd.append(yd) # NOTE: Tis will grow as N increases, fix.
#            #planet.md[planet_list.index(otherplanet)] = md
#            planet.md[j] = md
#            planet.rd[j] = rd
#            planet.yd[j] = yd # coord differences last to easily add z
#            planet.xd[j] = xd
#           
#            # dv_x/dt = -GMsun/r^3*x
#            planet.forcex[j] = planet.md[j]*planet.xd[j]/planet.rd[j]**3
#            planet.forcey[j] = planet.md[j]*planet.yd[j]/planet.rd[j]**3
#            j =+ 1 # Need to index numerically for np arrays
    # refresh planet position, and forces
    refreshPlanets(planet_list)       
            
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
        
#        planet.x_acc_old = (np.sum(planet.forcex)/planet.m)*4*np.pi**2
#        planet.y_acc_old = (np.sum(planet.forcey)/planet.m)*4*np.pi**2
        planet.x_acc_old = (np.sum(planet.forcex))*4*np.pi**2
        planet.y_acc_old = (np.sum(planet.forcey))*4*np.pi**2
        
       
        #x_old = planet.x
        #planet.x = planet.x + h*planet.vx # Euler pos update
#        planet.x = planet.x + h*planet.vx + h**2/2*(4*np.pi**2)*(np.sum(planet.forcex)/planet.m) # Verlet pos update
#        planet.y = planet.y + h*planet.vy + h**2/2*(4*np.pi**2)*(np.sum(planet.forcey)/planet.m)
        planet.x = planet.x + h*planet.vx + h**2/2*(4*np.pi**2)*(np.sum(planet.forcex)) # Verlet pos update
        planet.y = planet.y + h*planet.vy + h**2/2*(4*np.pi**2)*(np.sum(planet.forcey))
 
       #planet.vx = planet.vx - h*4*np.pi**2*(x_old/planet.r**3 + np.sum(planet.forcex))
        #planet.vx = planet.vx + h/2((x_acceleration_old) + (x_acceleration))
        
        # Since position must be updated before new velocity calc, also update r
        planet.genR() # This will update r with the new r from new x and y    
        
    # Take a break, refresh the position, combined forces, then calculate new velocity
    refreshPlanets(planet_list)
    # NOTE: When doing a comparison, this extra refresh MAY slow down any speed improvements/per accuracy compared to Euler
    # Might need to improve efficiency
    
    for planet in planet_list:
#        y_old = planet.y
#        planet.y = planet.y + h*planet.vy
#        planet.vy = planet.vy - h*4*np.pi**2*(y_old/planet.r**3 + np.sum(planet.forcey))
#        x_acc = (np.sum(planet.forcex)/planet.m)*4*np.pi**2
#        y_acc = (np.sum(planet.forcey)/planet.m)*4*np.pi**2
        x_acc = (np.sum(planet.forcex))*4*np.pi**2
        y_acc = (np.sum(planet.forcey))*4*np.pi**2
        planet.vx = planet.vx + h/2*((planet.x_acc_old) + (x_acc))
        planet.vy = planet.vy + h/2*((planet.y_acc_old) + (y_acc))
    
        planet.genR()
        
    refreshPlanets(planet_list)    
    
    t += h
    i += 1
    
#Plottr.plot(xe_arr, ye_arr)
#Plottr.plot(Earth.x_arr, Earth.y_arr)
#Plottr.plot(Jupiter.x_arr, Jupiter.y_arr)
for planet in planet_list:
    Plottr.plot(planet.x_arr, planet.y_arr, 'xpos', 'ypos', planet.name + ' Trajectory')

plt.figure()
for planet in planet_list:
    plt.plot(planet.x_arr, planet.y_arr)
plt.title('bigplot')
plt.xlabel('xpos')
plt.ylabel('ypos')
plt.show()