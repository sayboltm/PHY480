# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 12:38:40 2017
Project 3: Euler Method

V2.0 moves a bunch of static things to another file, that can also be used with
the Verlet algorithm

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
sys.path.append('../../')
import Plottr

###
plt.close("all") #close all; </matlab>
#mlab.close(all=True)
###


from solar_system import *

AU = 1.5e11
N = 15000 # mesh points


# These are defined in solar_system. Less readable at first, but cleaner and easier to implement
#planet_list = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune,
#               Pluto]
planet_list = [Mercury, Earth, Mars, Jupiter] # shorter list for debugging
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
    
    # Experimental: go back and add arrays because don't want N in other file
    planet.x_arr = np.zeros(N)
    planet.y_arr = np.zeros(N)
    planet.vx_arr = np.zeros(N)
    planet.vy_arr = np.zeros(N)
    planet.r_arr = np.zeros(N)
    
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
            md, rd, xd, yd = planet.diffPlanet(planet, otherplanet)
            # Can't do this for np arr
            #planet.md[planet_list.index(otherplanet)] = md 
            planet.md[j] = md
            planet.rd[j] = rd
            planet.yd[j] = yd # coord differences last to easily add z
            planet.xd[j] = xd
           
            # = other.m/m_sun * (current.x - other.x)/((current.x-other.x)**2 + (current.y-other.y)**2)**3
            # = md*xd/rd**3
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
        planet.x_arr[i] = planet.x # Store current values to array to plot later
        planet.y_arr[i] = planet.y
        planet.vx_arr[i] = planet.vx
        planet.vy_arr[i] = planet.vy
        # This got confusing so writing out the process to multiple planets 
        ''' Binary: dvx/dt = -GMsun/r^3*x, dx/dt = vx
                        GMsun = 4pi^2
                    dvx/dt = -4pi^2/r^3*x, dx/dt = vx
                    
                    Euler:
                    x_i+1 = x_i + h*vx_i
                    vx_i+1 = vx_i - d(vx_i)/dt
                    
                    x_i+1 = x_i + h*vx_i
                    vx_i+1 = vx_i - h*4pi^2/r_i^3*x_i
                    
                    vx_i+1 = vx_i - h*4pi^2*(x_i/r_i^3)
                    
                    
                    Verlet:
                    x_i+1 = x_i + h*vx_i + h^2/2*d(vx_i)/dt
                     
                    x_i+1 = x_i + h*vx_i + h^2/2*( -4pi^2/r_i^3*x_i )
                    vx_i+1 = vx_i + h/2*(( -4pi^2/r_i+1^3*x_i+1 ) + (-4pi^2/r_i^3*x_i))
                    
            Moarplanets: dvx/dt = -4pi^2/r^3*xe - 4pi^2(m_other/msun)/r^3_e-j * (xe-xj)
                                = -4*pi^2(x/r^3 + sum(md/rd*xd))
                                
                    Euler:
                    vx_i+1 = vx_i - h*( 4pi^2/r_i^3*x_i - 4pi^2(m_other/m_sun)/r^3_e-j * (xe-xj) )
                    vx_i+1 = vx_i - h*( 4pi^2/r_i^3*x_i - 4pi^2(m_other/m_sun)/r_i^3_ej * (xe_i-xj_i) )
                    vx_i+1 = vx_i - h*( 4pi^2/r_i^3*x_i - 4pi^2(md)/rd_i^3 * xd_i )
                    vx_i+1 = vx_i - h*4pi^2( x_i/r_i^3 - sum(md_i/rd_i^3*xd_i) )
                    
                    Verlet:
                    vx_i+1 = vx_i + h/2*(( -4pi^2/r_i+1^3*x_i+1 + sum(md_i+1/rd_i+1^3*xd_i+1)) + (-4pi^2/r_i^3*x_i + sum(md_i/rd_i^3*xd_i)))
        '''
        x_old = planet.x
        ### Euler: x_i+1
        planet.x = planet.x + h*planet.vx
        # forcex = other.m/m_sun * (current.x - other.x)/((current.x-other.x)**2 + (current.y-other.y)**2)
        #   = md*xd/rd**3
#        planet.vx = planet.vx - h*4*np.pi**2*(x_old/planet.r**3 + np.sum(planet.forcex))
        planet.vx = planet.vx - h*4*np.pi**2*(planet.x/planet.r**3 + np.sum(planet.forcex))
        ## Second is improved Euler
        
        
        y_old = planet.y
        planet.y = planet.y + h*planet.vy
#        planet.vy = planet.vy - h*4*np.pi**2*(y_old/planet.r**3 + np.sum(planet.forcey))
        planet.vy = planet.vy - h*4*np.pi**2*(planet.y/planet.r**3 + np.sum(planet.forcey))
        
        #r = np.sqrt(x**2 + y**2)
        planet.genR() # This will update earth.r with the new r from new x and y    
    
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
