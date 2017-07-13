#!/usr/bin/env python

''' Program will simulate transactions between random agents. 
Assumptions:
N agents exchange money in pairs
All agents start with same amount of money m0 > 0
at given timestep, random agents exchange random (uniform) amount of money '''

''' Changelog:
V1.1 Added num_experiments to run multiple experiments of N agents
V1.2 works kind of up to part b
    - fixed summation bug (never comitted)
V1.3 Add transactions and savings
V1.4 DONE Nearest neighbor interactions (similar wealth)
    V1.4.1 Corrected caveatSimilarWeath 
V1.5 Previous transaction likelihood
V2.0 Modularized, moved many functions to LibFinance
    - renamed some variables to match text
V2.1 Added separate plotting functions to str/ldr for big MC runs
'''
#### clear;
from IPython import get_ipython
get_ipython().magic('reset -sf')
#####

import numpy as np
import random as r
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
from datetime import datetime

import sys
sys.path.append('../../../') # Add path out of project folder to grab Plottr.py
sys.path.append('../') # add path just outside so don't have to copy financialib
import Plottr
import LibFinance as lf


###
plt.close("all") #close all; </matlab>
#mlab.close(all=True)
###


##### USER PARAMS ######
# Numer of agents in simulation:
N = 500

# start money for all agents
m0 = 1000

# Number of transactions
num_transactions = 10**5 # less transactions for debugging
#N = 10**7 

# Total experiments
num_experiments = 10**3

### Experiment parameters ###
# Fraction of money to save (set = 0 to disable)
#sav = .9
sav = 0

# Mean money = to m0 since all start with same
mean_money = m0

# Alpha (discrimination of similar wealth, 0=none, 1 =some, 2= alot)
#a = 1 
a = 2

# Gamma: effect of previous transactions
gam = 0 # Setting this = 10 (high) makes them all get $100

# Working directory folder name: (be sure it exists first)
workingdir = 'output'
write_to_file = 1 
histbins = 100 # Number of bins on histogram
plot_data = 1
##############################################################################
# Setup agents
#agents = np.zeros(num_agents)
#agents_avg  = np.zeros(N)
#agents[:] = m0

agents_storage = np.zeros((N,num_experiments))
variance_storage = np.zeros((num_transactions, num_experiments))
pct_10 = num_experiments/10



#Start timer
begintime = datetime.now()

# Begin experiment(s)
for kk in range(num_experiments):
    # Setup exchange log
    c = np.zeros((N,N)) # do this every experiment!!!!

    # Store result for averaging
    agents_storage[:,kk], variance_storage[:, kk] = lf.exchangeMoney(N, m0, 
            num_transactions, sav, mean_money, a, c, gam)
    # Print progress. Good for long runs
    #print(str(kk+1) + '/' + str(num_experiments) + ' experiments done.')
    if kk % pct_10 == 0:
        print(str(kk+pct_10) + '/' + str(num_experiments) + ' experiments done.') 

# End timer
print(datetime.now() - begintime)

## Average the experiments ( This probably isn't the right way to avg)
agents_total = np.ravel(agents_storage, 1)

#####################
# Save data
if write_to_file == 1:
    #working_vars = ['agents_storage', 'agents_total', 'variance_storage']
    working_vars = ['agents_storage', 'agents_total']
    for item in working_vars:
        np.savetxt(workingdir + '/' + item + '.txt', eval(item))

if plot_data == 1:
    lf.plotAll(agents_storage, agents_total, variance_storage, histbins)

# Test savetext
#np.savetxt('test.txt', agents_storage)

#Need to have:
#    this program save its data to text files (in case plots die)
#    this program call a plotting function with its loaded arrays
#    Another program capable of loading the text files, then calling same
#    plotting function
############################# Doesn't work properly/not what supposed to be
### Plot avg all experiments
#Plottr.plot(np.arange(len(agents_avg)), agents_avg, 'Agents', '$$$', 
#        'Raw plot of monies(All)')
#
#plt.figure()
#plt.hist(agents_avg)
#plb.xlabel('Money amount ($)')
#plb.ylabel('Frequency')
#plb.title('Occurance of certain amount of money(All)')
##plt.show(block=False) # show but allow input (and python to quit and leave plot)
#
## Plot the log histogram (part b)
#data, bins = np.histogram(agents_avg)
#Plottr.plot(bins[:-1], np.log10(data))
#plt.show(block=False)
