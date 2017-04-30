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
V1.3 IN-PROGRESS Add transactions and savings
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
N = 10**5 # less transactions for debugging
#N = 10**7 

# start money for all agents
m0 = 100

# Fraction of money to save
sav = .3

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

# Setup agents
#agents = np.zeros(num_agents)
agents_avg  = np.zeros(num_agents)
#agents[:] = m0

agents_storage = np.zeros((num_agents,num_experiments))

pct_10 = num_experiments/10
# Begin experiment(s)
def exchangeMoney(num_agents, m0, num_transactions):
    agents = np.zeros(num_agents)
    agents[:] = m0
    for k in range(num_transactions):
        # Pick two agents at random, numbered i and j
        i, j = agentPick(num_agents)
        
        # Generate a random number epsilon
        ep = epsilonGen()
        
        # Exchange money
        agents_i_old = agents[i]
#        agents[i] = ep*(agents[i] + agents[j])
#        agents[j] = (1-ep)*(agents_i_old + agents[j])
        agents[i] = agents[i]*sav + ep*(1-sav)*(agents[i] + agents[j])
        agents[j] = agents[j]*sav + (1-ep)*(1-sav)*(agents_i_old + agents[j])
    return agents

for kk in range(num_experiments):
    # Store result for averaging
    agents_storage[:,kk] = exchangeMoney(num_agents, m0, N)
    
    # Print progress. Good for long runs
    #print(str(kk+1) + '/' + str(num_experiments) + ' experiments done.')
    if kk % pct_10 == 0:
        print(str(kk+pct_10) + '/' + str(num_experiments) + ' experiments done.') 

## Average the experiments ( This probably isn't the right way to avg)
#for i in range(num_agents):
#    agents_avg[i] = np.mean(agents_storage[i,:])
# No want to 'sum' up all of them, then analyze
agents_total = np.zeros((num_experiments * num_agents))
for i in range(num_experiments): # Convert from block matrix to linear vector
    agents_total[i*num_agents:i*num_agents+num_agents] = agents_storage[:,i]

#########

# Plot normal
#plt.plot(agents)
Plottr.plot(np.arange(num_agents), agents_storage[:,-1], 'Agents', '$$$', 
        'Raw plot of monies(last experiment)')
# Plot histogram
#hist, bin_edges = np.histogram(agents)
plt.figure()
plt.hist(agents_storage[:,-1])
plb.xlabel('Money amount ($)')
plb.ylabel('Frequency')
plb.title('Occurance of certain amount of money(last experiment)')
#plt.show() # Only call plt.show() after all plots plotted

## Plot results of all experiments
#Plottr.plot(np.arange(len(agents_avg)), agents_avg, 'Agents', '$$$', 
#        'Raw plot of monies(All)')
plt.figure()
plt.hist(agents_total)
plb.xlabel('Money amount ($)')
plb.ylabel('Frequency')
plb.title('Occurance of certain amount of money(All Experiments)')
#plt.show(block=False) # show but allow input (and python to quit and leave plot)

# Plot the log histogram (part b)
data, bins = np.histogram(agents_total)
Plottr.plot(bins[:-1], np.log10(data))
plt.show(block=False)


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
