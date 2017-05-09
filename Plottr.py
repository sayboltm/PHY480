# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 15:33:41 2016

Scientific/plotting function library

DUPLICATE SLAVE FOR PHY480 (update one in old dropbox folder.. move to git eventually)

DONE: No need to Integrate updates 4/28/17
Changelog:
    - added plt.show() at end of plot()
    NO. don't do this.
@author: Mike
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as plb

def plot(X, Y=None, x_label=' ', y_label = ' ', title = ' ', xlog=0, ylog=0):
    ''' 2D plotting function '''
    # Sick of typing out plt.crap
    ''' Description: Needs at least X to plot, rest of arguments are optional, but if used, must be in order or set to defaults to 'skip'. '''
    plt.figure() # Make new fig just in case
    if Y == None:
        plt.plot(X)
    else:
        plt.plot(X, Y)
    plb.xlabel(x_label)
    plb.ylabel(y_label)
    plb.title(title)
	# Put some useful grid lines
    plt.grid(b=True, which='major', linestyle='-', linewidth=0.5)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', linestyle='-', linewidth=0.1)    
    if xlog == 1:
        plt.xscale('log')
    if ylog == 1:
        plt.yscale('log')
    plt.show(block=False)

def ImShow(array, xlabel='', ylabel='', title='', limits=None, docolorbar=0):
    ''' 2D array plot via ImShow '''
    plt.figure()   
	# imshow usually used for images, which by convention, are 'backwards' from what we'd expect
	# This is why origin = 'lower', and why the array is also transposed.
    if limits != None:
        plt.imshow(np.transpose(array), origin = 'lower', extent = limits)
    else:
        plt.imshow(np.transpose(array), origin = 'lower') # check out aspect=
    plt.show(block=False)
    plb.title(title)
    plb.xlabel(xlabel)
    plb.ylabel(ylabel)
    if docolorbar == 1:
		#plt.colorbar()
		#for robustness when running from console, cannot just call arbitrarily
        ax = plt.gca() # Get current axes
        plt.colorbar(ax=ax) 
        
            
