# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:22:54 2017
program too messy, move non-changing planets to separate file
@author: Mike
"""
import numpy as np

class Planet:
    ''' Planet class '''
    m_sun = 1.989e30 # kg

    def __init__(self, name, x, y, z, vx, vy, vz, m):
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
#        self.x_arr = np.zeros(N)
#        self.y_arr = np.zeros(N)
#        self.vx_arr = np.zeros(N)
#        self.vy_arr = np.zeros(N)
#        self.r_arr = np.zeros(N)
        
    def genR(self):
        # Call this to actually update r with the new x and y
        self.r = np.sqrt(self.x**2 + self.y**2)
        
#    def whoami(self):
#        return type(self).__name__
        
#    def __repr__(self):
#        return str(self)

    def diffPlanet(self, current, other):
        m_sun = 1.989e30
    
        md = other.m/m_sun
        xd = current.x - other.x
        yd = current.y - other.y
        rd = np.sqrt((current.x-other.x)**2 + (current.y-other.y)**2)
    
        return md, rd, xd, yd     
    
#M_sun = 2e30 # kg
#M_earth = 6e24
#AU = 1.5e11
#N = 15000 # mesh points



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
   

Mercury = Planet('Mercury', 8.968367955950400E-02, 2.992196150489325E-01,
                 1.599362695939906E-02, -3.263506651781252E-02,
                 8.994926847931269E-03, 3.728209609803519E-03, 3.285e23)

Venus = Planet('Venus', -7.157250830876660E-01, -5.463746561907697E-03,
               4.119492719005560E-02, 1.571327619572131E-04,
               -2.030702486642804E-02, -2.877803459876483E-04, 4.867e24)

Earth = Planet('Earth', -9.927202732475465E-01, -3.572900718985997E-02,
               -1.457459024144764E-04, 4.051841001203786E-04,
               -1.725183415131579E-02, 1.301878530083015E-06, 6e24)
   
Mars = Planet('Mars', 6.964271442280220E-01, 1.336186237410552E+00,
              1.074113383386008E-02, -1.188514840056006E-02,
              7.661099748032458E-03,  4.520818773004982E-04, 6.39e23)

Jupiter = Planet('Jupiter', -5.218545007266457E+00, -1.573296133029459E+00,
                 1.232426758421258E-01, 2.089612419969210E-03,
                 -6.867936621102540E-03, -1.826325534616215E-05, 1.898e27)

Saturn = Planet('Saturn', -1.444219825937719E+00, -9.941663023738931E+00,
                2.303359552729894E-01, 5.214363552028829E-03,
                -8.202877354316839E-04, -1.929777394638974E-04, 5.683e26)

Uranus = Planet('Uranus', 1.821297304478037E+01, 8.107332098409824E+00,
                -2.058417371481961E-01, -1.628389773951803E-03,
                3.409882688003075E-03, 3.384857367884728E-05, 8.681e25)

Neptune = Planet('Neptune', 2.841901110626624E+01, -9.447028517683961E+00,
                 -4.604010687768234E-01, 9.694142585199833E-04,
                 2.997924119743549E-03, -8.374103237166192E-05, 1.024e26)

Pluto = Planet('Pluto', 9.911780279031699E+00, -3.177666918637830E+01,
               5.332377813548366E-01, 3.072019865872833E-03,
               2.921185031268098E-04, -9.159655153717684E-04, 1.309e22)
               
PlanetX = Planet('PlanetX', 1,0,0,0,1,0,9000) # A test planet for screwing with classes