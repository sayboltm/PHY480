#!/usr/bin/env python
'''
Library for financial transaction simulator because main code too big
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import random as r

import sys
sys.path.append('../../')
import Plottr

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
    similar_wealth = 1
    previous_transactions = 0

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



##############################################################################
# Functions to store, load, and plot the data

# This is in here so it never gets changed and will remain constant between the
# main processing program, and the separate, plot-it-later program

def loadAll():
    pass



def plotAll(agents_storage, agents_total, variance_storage, histbins):
    # Derive some quantities from these given vars
    num_experiments = np.size(variance_storage[0,:])
    N = np.size(agents_storage[:,0])

    # Plot variance 
    plt.figure()
    for i in range(num_experiments):
        plt.plot(variance_storage[:, i])
    plt.xlabel('Monte Carlo Iterations')
    plt.ylabel('Variance')
    plt.title('Variance Over Monte Carlo Progression')
    plt.show()

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
    #plt.show(block=False) # show but allow input (and python to quit and leave plot)

    # Plot the log histogram (part b)
    data, bins = np.histogram(agents_total, bins=histbins)
    Plottr.plot(bins[:-1], np.log10(data))
    plt.show(block=False)


