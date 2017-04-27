#!/usr/bin/env python

''' Program will simulate transactions between random agents. 
Assumptions:
N agents exchange money in pairs
All agents start with same amount of money m0 > 0
at given timestep, random agents exchange random (uniform) amount of money '''

import numpy as np
import random as r
import matplotlib.pyplot as plt

##### USER PARAMS ######
#Agents:
num_agents = 500

# Number of transactions
N = 10**2 # should be 10**7

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

# Setup agents
agents = np.zeros(num_agents)
agents[:] = m0

# Begin experiment
for k in range(N):
    
    # Pick two agents at random, numbered i and j
    i, j = agentPick(num_agents)
    
    # Generate a random number epsilon
    ep = epsilonGen()
    
    # Exchange money
    agents[i] = ep*(agents[i] + agents[j])
    agents[j] = (1-ep)*(agents[i] + agents[j])
    
    
# Plot histogram
hist, bin_edges = np.histogram(agents)

