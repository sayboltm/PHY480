#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Description
Jacobi's method
'''

import numpy as np

ep = 0.1

# Go until ||Ax^(n)-b|| is small

                
A = np.array([[2,1],[5,7]])
b = np.array([[11],[13]])

# Initial guess to solution
x = np.array([[1],[1]])



