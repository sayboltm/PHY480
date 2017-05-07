#!/usr/bin/env python
'''
Library for financial transaction simulator because main code too big
'''
import numpy as np
import random as r

def epsilonGen(distribution='uniform'):
    ''' Generate random number epsilon for determining how much money is
    exchanged '''
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

#def exchangeMoney(num_agents, m0, num_transactions):
#    agents = np.zeros(num_agents)
#    agents[:] = m0
#    for k in range(num_transactions):
#        # Pick two agents at random, numbered i and j
#        i, j = agentPick(num_agents)
#        
#        # Generate a random number epsilon
#        ep = epsilonGen()
#        
#        # Exchange money
#        agents_i_old = agents[i]
##        agents[i] = ep*(agents[i] + agents[j])
##        agents[j] = (1-ep)*(agents_i_old + agents[j])
#        agents[i] = agents[i]*sav + ep*(1-sav)*(agents[i] + agents[j])
#        agents[j] = agents[j]*sav + (1-ep)*(1-sav)*(agents_i_old + agents[j])
#    return agents

def exchangeMoney(N, m0, num_transactions, sav, mean_money, a, c, gam):
    ''' Attempt to exchange money with some caviat after selection. This caveat
    may be agents must be of similar wealth, or have done a transaction
    previously '''
    agents = np.zeros(N)
    agents[:] = m0
    
    # Track the variance
    var = np.zeros(num_transactions)

    for k in range(num_transactions):
        # Pick two agents at random, numbered i and j
        i, j = agentPick(N) # This is still the same
        
        # Generate a random number epsilon
        ep = epsilonGen()
        
        # Exchange money | New: if probability agrees with it
#        interact = caveatSimilarWealth(agents, i, j, m0, a)
        # TODO: similar wealth throwing error and it didn't before
#        interact = caveatPreviousTransactions(agents, i, j, c, gam)
        interact = caveatFunction(agents, i, j, mean_money, a, c, gam)

        if interact == 1: # Else, don't exchange money
            agents_i_old = agents[i]
            agents[i] = agents[i]*sav + ep*(1-sav)*(agents[i] + agents[j])
            agents[j] = agents[j]*sav + (1-ep)*(1-sav)*(agents_i_old + agents[j])
            # log it too
            c[i,j] += 1
            c[j,i] += 1
            
        # and variance at end of each run 
        var[k] = np.var(agents)

    return agents, var

def caveatFunction(agents, i, j, mean_money, a, c, gam):
    ''' A generic caveat function so one can apply discrimination based on
    similar wealth or previous transactions or both or none '''
    # Discriminate based on:
    similar_wealth = 0
    previous_transactions = 1

    if (similar_wealth == 1) and (previous_transactions == 0):
        p_interact = similarWealth(agents, i, j, mean_money, a)
    elif (similar_wealth == 0) and (previous_transactions == 1):
        p_interact = previousTransactions(agents, i, j, c, gam)
    elif (similar_wealth == 1) and (previous_transactions == 1):
        p1 = similarWealth(agents, i, j, mean_money, a)
        p2 = previousTransactions(agents, i, j, c, gam)
        p_interact = p1*p2
    else:
        p_interact = 1
    
    p_no_interact = 1-p_interact
    interact = np.random.choice(np.arange(2), p=[p_no_interact, p_interact])
    return interact

def similarWealth(agents, i, j, mean_money, a):
    mi = agents[i]
    mj = agents[j]
    x = np.abs((mi-mj)/mean_money)
    # The 1 in 'x+1' could also be varied in the future
    p_interact = 1-(x/(x+1))**a 
    return p_interact

def previousTransactions(agents, i, j, c, gam):
    return ((c[i,j] + 1)/(np.max(c) + 1))**gam




### Depricated crap ###
def caveatSimilarWealth(agents, i, j, mean_money, a):
    ''' A Function to decide on interaction based on similar wealth
        Where:
            agents: vector of agents
            i: first agent picked
            j: index of second agent picked
            mean_money: average money of agents
            a: discrimination based on money
                0 = disabled
                small = some discrimination
                a > 1: only agents with very similar wealth will interact

The paper's function was for random initial money, not all the same which
is why this modification is required. '''
    # Where pij is probability of INTERACTION
#    pij = np.tanh(np.abs((agents[i]-agents[j])/mean_money)**-a)
    mi = agents[i]
    mj = agents[j]
    x = np.abs((mi-mj)/mean_money)
    pij = 1-(x/(x+1))**a # The 1 in 'x+1' could also be varied in the future
    p_interact = pij
    p_no_interact = 1-pij
    # Decide if interact or not
    interact = np.random.choice(np.arange(2), p=[p_no_interact, p_interact])
    return interact

def caveatPreviousTransactions(agents, i, j, c, gam):
    # Construct a matrix of cij of all transactions. Each time an agent interacts, they increment their index by one
    pij = ((c[i,j] + 1)/(np.max(c) + 1))**gam

    p_interact = pij
    p_no_interact = 1-pij 
    interact = np.random.choice(np.arange(2), p=[p_no_interact, p_interact])
    return interact

