#!/usr/bin/env python

'''Quickplot: A program to load from text file and call the same plotting
function the main one does '''
# Experimental edition: just plot all this stuff pulled from server asap
# V2.0 if you can call it that... tear it apart to get desired plots.
# WARNIG: this code is ugly and desperate
# manual version: named folders dumb things to have to hard code import as
# something else.
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
#working_dir = '../../PHY480tmp/defaultlol/output' # redoing
#working_dir = '../../PHY480tmp/sav.25/output'
#working_dir = '../../PHY480tmp/sav.5/output'
#working_dir = '../../PHY480tmp/sav.9/output'
#working_dir = '../../PHY480tmp/a.5/output'
#working_dir = '../../PHY480tmp/a1/output'
#working_dir = '../../PHY480tmp/a1.5/output'
#working_dir = '../../PHY480tmp/a2/output' # Redoing
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
#working_dir = '../../PHY480tmp/mod/a2g2/output' # fack this is fucked too
#working_dir = '../../PHY480tmp/mod/a2g3/output'
#working_dir = '../../PHY480tmp/mod/a2g4/output'
#working_dir = '../../PHY480tmp/mod/a2g5/output'

# Things to import, which will be plotted.
# This should be modular but its not, no time to screw with that for 3 vars
#working_vars = ['agents_storage', 'agents_total', 'variance_storage']

working_vars = ['agents_storage', 'agents_total']

dir_prefix = '../../PHY480tmp/mod/'
dir_prefix = '../../PHY480tmp/'
#working_dirs = ['a1g0','a1g1','a1g2','a1g3','a1g4','a1g5']
#working_dirs = ['a2g0','a2g1','a2g2','a2g3','a2g4','a2g5']
working_dirs = ['a1g0','a1g1','a1g2','a1g3','a1g4','a1g5','a2g0','a2g1',
        'a2g2','a2g3','a2g4','a2g5']
histbins = 100

## apparently creating vars this way is extremely dangerous, but it works
#for adir in working_dirs:
#    for avar in working_vars:
#        globals()[adir+'_'+avar] = np.loadtxt(dir_prefix + adir + '/output/' +
#                avar + '.txt')
## See:
#http://stupidpythonideas.blogspot.com/2013/05/why-you-dont-want-to-dynamically-create.html
ahalf_agents_storage = np.loadtxt(dir_prefix + 'a.5' + '/output/' + 
        'agents_storage' + '.txt')
ahalf_agents_total = np.loadtxt(dir_prefix + 'a.5' + '/output/' + 
        'agents_total' + '.txt')

a1_agents_storage = np.loadtxt(dir_prefix + 'a1' + '/output/' + 'agents_storage' + '.txt')
a1_agents_total = np.loadtxt(dir_prefix + 'a1' + '/output/'
        +'agents_total' + '.txt')

a1half_agents_storage = np.loadtxt(dir_prefix + 'a1.5' + '/output/' + 'agents_storage' + '.txt')
a1half_agents_total = np.loadtxt(dir_prefix + 'a1.5' + '/output/' +
'agents_total' + '.txt')

a2_agents_storage = np.loadtxt(dir_prefix + 'a2' + '/output/' + 'agents_storage' + '.txt')
a2_agents_total = np.loadtxt(dir_prefix + 'a2' + '/output/' + 'agents_total' + '.txt')
#lf.plotAll(agents_storage, agents_total, variance_storage, histbins)

# modify working dirs to work with this crap
working_dirs = ['ahalf', 'a1', 'a1half', 'a2']

#def plotLog():
# Plot the logs from various datasets on top of each other
# Easier to do outside of function because dealing with these dangerously
# created vars is tricky
#### This piece of dangerous magic works beautifully! ######
#for adir in working_dirs:
#    plt.figure()
#    data, bins = np.histogram(eval(adir + '_agents_total'), bins=histbins)
#    plt.plot(bins[:-1], np.log10(data))
#    plb.xlabel('Money amount ($)')
#    plb.ylabel('$log_{10}(Frequency)$')
#    plb.title(adir)
#    plt.show(block=False)

# Now, try to actually plot the logs alongside each other
plt.figure()
for adir in working_dirs:
    data, bins = np.histogram(eval(adir + '_agents_total'), bins=histbins)
    plt.plot(bins[:-1], np.log10(data), label=adir)
plb.xlabel('Money amount ($)')
plb.ylabel('$log_{10}(Frequency)$')
plb.title('Distribution of Wealth (log) for Various $\gamma$')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show(block=False)

# nonlog version
plt.figure()
for adir in working_dirs:
    data, bins = np.histogram(eval(adir + '_agents_total'), bins=histbins)
    plt.plot(bins[:-1], data, label=adir)
plb.xlabel('Money amount ($)')
plb.ylabel('Frequency')
plb.title('Distribution of Wealth for Various $\\alpha$ and $\gamma$')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show(block=False)
#
# Try an imshow plot?!
#test = np.zeros((len(working_dirs),histbins))
#limits=[0,5,0,5]
#i=0
#for adir in working_dirs:
#    data, bins = np.histogram(eval(adir + '_agents_total'), bins=histbins)
#    test[i,:] = np.log10(data)
#    i += 1
#Plottr.ImShow(test, '$\gamma$','incorrecscaleM','title',None, 1)
# Doesn't give much extra insight

def dontPlotAll(agents_storage, agents_total, histbins):
   # Derive some quantities from these given vars
    num_experiments = np.size(variance_storage[0,:])
    N = np.size(agents_storage[:,0])

    # Plot variance 
    plt.figure()
    for i in range(num_experiments):
        plt.plot(variance_storage[:, i])
    plt.xlabel('Number of Transactions')
    plt.ylabel('Variance')
    plt.title('Variance During Monte Carlo Progression')
    plt.show(block=False)

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


#dontPlotAll(agents_storage, agents_total, histbins)
