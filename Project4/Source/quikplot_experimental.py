#!/usr/bin/env python

'''Quickplot: A program to load from text file and call the same plotting
function the main one does '''
# Experimental edition: just plot all this stuff pulled from server asap


#### clear;
from IPython import get_ipython
get_ipython().magic('reset -sf')
#####

import LibFinance as lf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as plb

import sys
sys.path.append('../../')
import Plottr

###
plt.close("all") #close all; </matlab>
#mlab.close(all=True)
###


# The folder to grab stuff from
#working_dir = 'output'
#working_dir = '../../PHY480tmp/defaultlol/output' 
#working_dir = '../../PHY480tmp/sav.25/output'
#working_dir = '../../PHY480tmp/sav.5/output'
#working_dir = '../../PHY480tmp/sav.9/output'
#working_dir = '../../PHY480tmp/a.5/output'
#working_dir = '../../PHY480tmp/a1/output'
#working_dir = '../../PHY480tmp/a1.5/output'
#working_dir = '../../PHY480tmp/a2/output' 
#working_dir = '../../PHY480tmp/a10/output'

#working_dir = '../../PHY480tmp/mod/a1g0/output'
#working_dir = '../../PHY480tmp/mod/a1g1/output'
#working_dir = '../../PHY480tmp/mod/a1g2/output'
#working_dir = '../../PHY480tmp/mod/a1g3/output'
#working_dir = '../../PHY480tmp/mod/a1g4/output'
#working_dir = '../../PHY480tmp/mod/a1g5/output'
#
#working_dir = '../../PHY480tmp/mod/a2g0/output'
#working_dir = '../../PHY480tmp/mod/a2g1/output'
working_dir = '../../PHY480tmp/mod/a2g2/output' 
#working_dir = '../../PHY480tmp/mod/a2g3/output'
#working_dir = '../../PHY480tmp/mod/a2g4/output'
#working_dir = '../../PHY480tmp/mod/a2g5/output'

# Things to import, which will be plotted.
# This should be modular but its not, no time to screw with that for 3 vars
#working_vars = ['agents_storage', 'agents_total', 'variance_storage']

working_vars = ['agents_storage', 'agents_total']
histbins = 100

# apparently creating vars this way is extremely dangerous, but it works
for item in working_vars:
    globals()[item] = np.loadtxt(working_dir + '/' + item + '.txt')
# See:
#http://stupidpythonideas.blogspot.com/2013/05/why-you-dont-want-to-dynamically-create.html

#lf.plotAll(agents_storage, agents_total, variance_storage, histbins)

def dontPlotAll(agents_storage, agents_total, histbins):
    # Derive some quantities from these given vars
#    num_experiments = np.size(variance_storage[0,:])
    N = np.size(agents_storage[:,0])

#    # Plot variance 
#    plt.figure()
#    for i in range(num_experiments):
#        plt.plot(variance_storage[:, i])
#    plt.xlabel('Number of Transactions')
#    plt.ylabel('Variance')
#    plt.title('Variance During Monte Carlo Progression')
#    plt.show(block=False)
#
    # Plot normal
    #plt.plot(agents)
    Plottr.plot(np.arange(N), agents_storage[:,-1], 'Agents', '$$$', 
            'Raw plot of monies(last experiment)')
    # Plot histogram
    #hist, bin_edges = np.histogram(agents)
    plt.figure()
    plt.hist(agents_storage[:,-1],bins=histbins)
    plb.xlabel('Money amount ($)')
    plb.ylabel('Frequency')
    plb.title('Occurance of certain amount of money(last experiment)')
    #plt.show() # Only call plt.show() after all plots plotted

    ## Plot results of all experiments
    #Plottr.plot(np.arange(len(agents_avg)), agents_avg, 'Agents', '$$$', 
    #        'Raw plot of monies(All)')
    plt.figure()
    plt.hist(agents_total,bins=histbins)
    plb.xlabel('Money amount ($)')
    plb.ylabel('Frequency')
    plb.title('Occurance of certain amount of money(All Experiments)')
    plt.show(block=False) # show but allow input (and python to quit and leave plot)

    # Plot the log histogram (part b)
    data, bins = np.histogram(agents_total, bins=histbins)
    Plottr.plot(bins[:-1], np.log10(data))
    plb.xlabel('Money amount ($)')
    plb.ylabel('$log_{10}(Frequency)$')
    plb.title('Log plot of certain amount of money(All Experiments)')
    plt.show(block=False)


dontPlotAll(agents_storage, agents_total, histbins)
