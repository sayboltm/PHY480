#!/usr/bin/env python

'''Quickplot: A program to load from text file and call the same plotting
function the main one does '''

import LibFinance as lf
import numpy as np

# The folder to grab stuff from
working_dir = 'output'

# Things to import, which will be plotted.
# This should be modular but its not, no time to screw with that for 3 vars
working_vars = ['agents_storage', 'agents_total', 'variance_storage']
histbins = 100

# apparently creating vars this way is extremely dangerous, but it works
for item in working_vars:
    globals()[item] = np.loadtxt(working_dir + '/' + item + '.txt')
# See:
#http://stupidpythonideas.blogspot.com/2013/05/why-you-dont-want-to-dynamically-create.html

lf.plotAll(agents_storage, agents_total, variance_storage, histbins)

