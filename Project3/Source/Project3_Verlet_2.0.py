# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 12:38:40 2017
Project 3 binary system test

Project3_Verlet1.1_test2.py
it works! Saving as *Verlet_2.0, and cleaning up

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
#sys.path.append('~/GitHub/sayboltm/PHY480')
sys.path.append('/home/mike/GitHub/sayboltm/PHY480')
sys.path.append('../../') # This is more portable, cant seem to use ~ here
import Plottr

###
plt.close("all") #close all; </matlab>
#mlab.close(all=True)
###

from solar_system import *

AU = 1.5e11
N = 15000 # mesh points

''' These are lists of planets to be analyzed '''
#planet_list = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune,
#               Pluto]
planet_list = [Mercury, Earth, Mars, Jupiter] # shorter list for debugging
#planet_list = [Earth, Jupiter]
#planet_list = [Earth, Jupiter, PlanetX]
#planet_list = [Earth]


ts = 0
te = 4*np.pi#10#4*np.pi
h = (te-ts)/float(N)
t_arr = np.zeros(N)
t = ts # Init t to tstart = 0

# Test looping and skipping
for planet in planet_list:
    # Works as expected
    print('Current planet: ', planet.name)
    for otherplanet in planet_list:
        if otherplanet == planet: # If current planet, skip it
            continue
        print('\totherplanet: ', otherplanet.name)
        

# Setup some extra arrays in the planets
for planet in planet_list:
    planet.md = np.zeros(len(planet_list)-1) # 'MassDifference': otherplanet.m/m_sun ( see planet.diffPlanet)
    planet.rd = np.zeros(len(planet_list)-1) # 'RadiDifference': sqrt((currentx-otherx)^2 + (currenty-othery)^2)
    planet.xd = np.zeros(len(planet_list)-1) # 'Xdifference': currentX - otherX
    planet.yd = np.zeros(len(planet_list)-1) # 'Ydifference': 
    planet.forcex = np.zeros(len(planet_list)-1) # An additional force component since it needs to be summed as a whole in the velocity update
    planet.forcey = np.zeros(len(planet_list)-1) # -1 because this is the force from all other planets 
    for otherplanet in planet_list: 
        if otherplanet == planet:
            continue
        planet.diff_index.append(otherplanet.name) # used to track order of planet iteration, contains planets in order they are printed here
        # i.e. Earth.diff_index contains [Jupiter, PlanetX], and Earth.dx contains [DistEarthJupiter, DistEarthPlanetX] ...
   
    # Arrays of position and velocity for plotting/examining later
    planet.x_arr = np.zeros(N)
    planet.y_arr = np.zeros(N)
    planet.vx_arr = np.zeros(N)
    planet.vy_arr = np.zeros(N)
    planet.r_arr = np.zeros(N)
    
    # Need variable to store old acceleration (Verlet only)
    planet.x_acc_old = None
    planet.y_acc_old = None
    
''' Used to refresh the force components of other planets once each position has been updated
created for use in Verlet where velocity must be updated after ALL positions, but cleaner
implementation if used in Euler too. '''
def refreshPlanets(planet_list):
    for planet in planet_list:
        j = 0
        for otherplanet in planet_list:
            if otherplanet == planet: # skip if current planet as this function pertains to forces of other planets
                continue
            # diffPlanet depends on position only, not velocity so safe to update here
            md, rd, xd, yd = planet.diffPlanet(planet, otherplanet)
            planet.md[j] = md # update mass and other differences for each other planet j
            planet.rd[j] = rd
            planet.yd[j] = yd # x and y are last to easily add z later
            planet.xd[j] = xd
           
            # dv_x/dt = -GMsun/r^3*x = 
            planet.forcex[j] = planet.md[j]*planet.xd[j]/planet.rd[j]**3
            planet.forcey[j] = planet.md[j]*planet.yd[j]/planet.rd[j]**3
            j =+ 1 # Need to index numerically for np arrays
    
i = 0
#while (t < te):
for i in range(N): #moar reliable. Had issues with t being very close to te and taking an extra loop

    t_arr[i] = t
     
    # refresh planet position, and forces 
    refreshPlanets(planet_list)       
            
    for planet in planet_list: 
        ''' For Verlet, break up and do two for planet in planetlist, first updating 
        position, storing old acceleration, then updating velocity,
        recalculating acceleration as well as using the stored old value '''
        
        ''' Eventually need to move into planet.pos[0,1] instead of planet.x, 
        planet.y '''
    
        planet.x_arr[i] = planet.x # Store current values to array to plot later
        planet.y_arr[i] = planet.y
        planet.vx_arr[i] = planet.vx
        planet.vy_arr[i] = planet.vy 
        
#        planet.y_acc_old = (np.sum(planet.forcey)/planet.m)*4*np.pi**2
        # This is actually the 'acceleration component' for use later
        planet.x_acc_old = -4*np.pi**2/planet.r**3*planet.x + np.sum(planet.forcex)
        planet.y_acc_old = -4*np.pi**2/planet.r**3*planet.y + np.sum(planet.forcey)
        
       
        #x_old = planet.x
        #planet.x = planet.x + h*planet.vx # Euler pos update
        planet.x = planet.x + h*planet.vx + h**2/2*(-4*np.pi**2/planet.r**3*planet.x) # Verlet pos update
        planet.y = planet.y + h*planet.vy + h**2/2*(-4*np.pi**2/planet.r**3*planet.y)
 
        #planet.vx = planet.vx - h*4*np.pi**2*(x_old/planet.r**3 + np.sum(planet.forcex)) # Euler velocity update
        #planet.vx = planet.vx + h/2((x_acceleration_old) + (x_acceleration)) # Conceptual Verlet velocity update
        
        # Since position must be updated before new velocity calc, also update r
        planet.genR() # This will update r with the new r from new x and y    
        
    # Take a break, refresh the position, combined forces, then calculate new velocity
    refreshPlanets(planet_list)
    # NOTE: When doing a comparison, this extra refresh MAY slow down any speed improvements/per accuracy compared to Euler
    # Might need to improve efficiency
    
    for planet in planet_list:
#        planet.vy = planet.vy - h*4*np.pi**2*(y_old/planet.r**3 + np.sum(planet.forcey)) # Euler velocity update
#        x_acc = (np.sum(planet.forcex)/planet.m)*4*np.pi**2 # 1st verlet attempt
        #x_acc = (np.sum(planet.forcex))*4*np.pi**2 # 2nd attempt, stuck for a week
        x_acc = -4*np.pi**2/planet.r**3*planet.x + np.sum(planet.forcex) # Current acceleration (Works)
        y_acc = -4*np.pi**2/planet.r**3*planet.y + np.sum(planet.forcey)
        planet.vx = planet.vx + h/2*((planet.x_acc_old) + (x_acc)) # Verlet velocity update
        planet.vy = planet.vy + h/2*((planet.y_acc_old) + (y_acc))
    
        planet.genR() # Again, update R for each planet, then refresh planets at end of loop
        
    refreshPlanets(planet_list)    
    
    t += h
    i += 1
    
### Plot
#Plottr.plot(xe_arr, ye_arr)
#Plottr.plot(Earth.x_arr, Earth.y_arr)
#Plottr.plot(Jupiter.x_arr, Jupiter.y_arr)
for planet in planet_list:
    Plottr.plot(planet.x_arr, planet.y_arr, 'xpos', 'ypos', planet.name + ' Trajectory')

plt.figure()
for planet in planet_list:
    plt.plot(planet.x_arr, planet.y_arr)
plt.title('Multi-Planet Plot')
plt.xlabel('xpos')
plt.ylabel('ypos')
plt.show(block=False)
