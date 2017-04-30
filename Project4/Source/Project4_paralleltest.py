#!/usr/bin/env python

# Attempt at parallel code to speed up. didn't really work.

''' Program will simulate transactions between random agents. 
Assumptions:
N agents exchange money in pairs
All agents start with same amount of money m0 > 0
at given timestep, random agents exchange random (uniform) amount of money '''

''' Changelog:
V1.1 Added num_experiments to run multiple experiments of N agents
'''
#### clear;
from IPython import get_ipython
get_ipython().magic('reset -sf')
#####

import numpy as np
import random as r
import matplotlib.pyplot as plt
import matplotlib.pylab as plb

import sys
sys.path.append('../../') # Add path out of project folder to grab Plottr.py
import Plottr 

from joblib import Parallel, delayed
import multiprocessing
###
plt.close("all") #close all; </matlab>
#mlab.close(all=True)
###

##### USER PARAMS ######
#Agents:
num_agents = 500

# Total experiments
num_experiments = 10**2

# Number of transactions
#N = 10**2 # should be 10**7
#N = 10**7 # Everyone has $0?? Money not being conserved or something
#N = 10**4 # This works
N = 10**5 # Barely works
#N = 10**6 # doesn't work

# start money for all agents
m0 = 100

########################

# Random function for epsilon for modularity
def epsilonGen(distribution='uniform'):
    # bounds of epsilon
    bounds = [0,1]
    if distribution == 'uniform':
        return r.uniform(bounds[0], bounds[1]) # inclusive of bounds

def agentPick(num_agents):
    ''' Generate some agents i and j '''
    while(1):
        agent_i = r.randint(0, num_agents-1)
        agent_j = r.randint(0, num_agents-1)
        
        if agent_i != agent_j:
            break
#        else:
#            print('agents same. redoing')
    return agent_i, agent_j

# Exchange of money experiment, modularized so can be run on multi-cores
def exchangeMoney(num_agents, m0, num_transactions):
    agents = np.zeros(num_agents)
    agents[:] = m0
    for k in range(num_transactions):
        # Pick two agents at random, numbered i and j
        i, j = agentPick(num_agents)
        
        # Generate a random number epsilon
        ep = epsilonGen()
        
        # Exchange money
        # Need this:
        agents_i_old = agents[i]
        agents[i] = ep*(agents[i] + agents[j])
        agents[j] = (1-ep)*(agents_i_old + agents[j])# THIS IS WRONG
    return agents

# Setup agents
agents_avg  = np.zeros(num_agents)
agents_storage = np.zeros((num_agents,num_experiments))

pct_10 = num_experiments/10
# Begin experiment(s)

#for kk in range(num_experiments):
#    # Store result for averaging
#    agents_storage[:,kk] = exchangeMoney(N)
#    
#    # Print progress. Good for long runs
#    #print(str(kk+1) + '/' + str(num_experiments) + ' experiments done.')
#    if kk % pct_10 == 0:
#        print(str(kk+pct_10) + '/' + str(num_experiments) + ' experiments done.') 

num_cores = multiprocessing.cpu_count()
results = Parallel(n_jobs=num_cores)(delayed(exchangeMoney(num_agents, m0, N))(kk) for kk in range(num_experiments))

# Average the experiments ( This probably isn't the right way to avg)
#for i in range(len(agents)):
for i in range(num_agents):
    agents_avg[i] = np.mean(agents_storage[i,:])

# Plot normal
#plt.plot(agents)
Plottr.plot(np.arange(len(agents)), agents, 'Agents', '$$$', 'Raw plot of' + 
            ' monies')
# Plot histogram
#hist, bin_edges = np.histogram(agents)
plt.figure()
plt.hist(agents)
plb.xlabel('Money amount ($)')
plb.ylabel('Frequency')
plb.title('Occurance of certain amount of money')
#plt.show() # Only call plt.show() after all plots plotted

## Plot avg all experiments
Plottr.plot(np.arange(len(agents_avg)), agents, 'Agents', '$$$', 
        'Raw plot of monies(All)')

plt.figure()
plt.hist(agents_avg)
plb.xlabel('Money amount ($)')
plb.ylabel('Frequency')
plb.title('Occurance of certain amount of money(All)')
#plt.show(block=False) # show but allow input (and python to quit and leave plot)

# Plot the log histogram (part b)
data, bins = np.histogram(agents_avg)
Plottr.plot(bins[:-1], np.log10(data))
plt.show(block=False)
