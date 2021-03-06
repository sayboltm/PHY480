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
V1.4 IN PROGRESS Nearest neighbor interactions
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

from datetime import datetime

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

# Fraction of money to save (set = 0 to disable)
#sav = .9
sav = 0

# Mean money = to m0 since all start with same
mean_money = m0

# Alpha
#a = 1 
a = 2.7
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
        
        # Make sure picked agents are not the same
        if agent_i != agent_j:
            break
    return agent_i, agent_j

# Setup agents
#agents = np.zeros(num_agents)
agents_avg  = np.zeros(num_agents)
#agents[:] = m0

agents_storage = np.zeros((num_agents,num_experiments))

pct_10 = num_experiments/10

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

def exchangeMoneyCaveat(num_agents, m0, num_transactions, mean_money, a):
    ''' Attempt to exchange money with some caviat after selection.
    This caveat may be agents must be of similar wealth, or have done a 
    transaction previously. '''
    agents = np.zeros(num_agents)
    agents[:] = m0
    for k in range(num_transactions):
        # Pick two agents at random, numbered i and j
        i, j = agentPick(num_agents) # This is still the same
        
        # Generate a random number epsilon
        ep = epsilonGen()
        
        # Exchange money | New: if probability agrees with it
        interact = caveatSimilarMoney(agents, i, j, m0, a)

        if interact == 1: # Else, don't exchange money
            agents_i_old = agents[i]
            agents[i] = agents[i]*sav + ep*(1-sav)*(agents[i] + agents[j])
            agents[j] = agents[j]*sav + (1-ep)*(1-sav)*(agents_i_old + agents[j])
    return agents

def caveatSimilarMoney(agents, i, j, mean_money, a):
    ''' A Function to decide on interaction based on similar wealth
        Where:
            agents: vector of agents
            i: first agent picked
            j: index of second agent picked
            mean_money: average money of agents
            a: discrimination based on money
                0 = same output (but reduced by 1-(2*(1/e))
                small a will tend toward less discrimination
                big a only agents with very similar wealth will interact '''

    ''' pij = np.tanh(np.abs((mi-mj)/m0)**-a), where a = 0 to disable, but
    actually still reduces probability. Nice that bounded by 1, so easy to 
    work with. small a lessens the effect., big a, agents will back off for
    smaller differences.'''
    pij = np.tanh(np.abs((agents[i]-agents[j])/mean_money)**-a)
    # Where pij is probability of INTERACTION
    p_interact = pij
    p_no_interact = 1-pij
    # Decide if interact or not
    interact = np.random.choice(np.arange(2), p=[p_no_interact, p_interact])
    return interact

# Start timer
begintime = datetime.now()

# Begin experiment(s)
for kk in range(num_experiments):
    # Store result for averaging
#    agents_storage[:,kk] = exchangeMoney(num_agents, m0, N)
    agents_storage[:,kk] = exchangeMoneyCaveat(num_agents,m0, N,mean_money, a)
    # Print progress. Good for long runs
    #print(str(kk+1) + '/' + str(num_experiments) + ' experiments done.')
    if kk % pct_10 == 0:
        print(str(kk+pct_10) + '/' + str(num_experiments) + ' experiments done.') 

# End timer
print(datetime.now() - begintime)

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
plt.hist(agents_storage[:,-1],bins=20)
plb.xlabel('Money amount ($)')
plb.ylabel('Frequency')
plb.title('Occurance of certain amount of money(last experiment)')
#plt.show() # Only call plt.show() after all plots plotted

## Plot results of all experiments
#Plottr.plot(np.arange(len(agents_avg)), agents_avg, 'Agents', '$$$', 
#        'Raw plot of monies(All)')
plt.figure()
plt.hist(agents_total,bins=20)
plb.xlabel('Money amount ($)')
plb.ylabel('Frequency')
plb.title('Occurance of certain amount of money(All Experiments)')
#plt.show(block=False) # show but allow input (and python to quit and leave plot)

# Plot the log histogram (part b)
data, bins = np.histogram(agents_total, bins=20)
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
