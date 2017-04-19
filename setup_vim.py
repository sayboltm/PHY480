#!/usr/bin/env python
#####################
# '''setup_vim.py'''
# Desc: A program to setup VIM bc so many linux
# V 1.0 Beta
# 2/9/17

#### clear;
from IPython import get_ipython
get_ipython().magic('reset -sf')
#####

# TODO: Still need to uncomment lines in '/usr/share/vim/vimrc'
# TODO: Need to append file if already exist or not equal to desired prefs
import os
import re
# Re help see: HorzgcodeEleks, HFSS_Data_Analyzerv1.1, setup_vim

# Preferences to write to 'python.vim':
preferences = 'set tabstop=8\nset expandtab\nset shiftwidth=4\nset softtabstop=4'
filename = 'python.vim'

if os.path.isdir(os.path.expanduser('~/.vim/ftplugin/')) == False:
    print('[+] Dir not found: ' + os.path.expanduser('~/.vim/ftplugin/') + '.'
        + 'Making directories...')
    os.makedirs(os.path.expanduser('~/.vim/ftplugin'))
else:
    print('[+] Directory found: ' + os.path.expanduser('~/.vim/ftplugin/'))
#os.chdir(os.path.expanduser('~/.vim/ftplugin/'))

if os.path.exists(os.path.expanduser('~/.vim/ftplugin/python.vim')) == False:
    print('[+] Config file not found. Creating....')
    #os.chdir('~/.vim/ftplugin/')
    os.chdir(os.path.expanduser('~/.vim/ftplugin/'))
    with open(filename, 'w') as f:
        f.writelines(preferences)
    f.closed
else:
    print('[+] File already exist! Good to go.')

#print(os.path.isdir('~/.vim/ftpugin'))
#print(os.path.exists('~/.vim/'))
#print(os.path.isdir('~/.vim/'))
#print(os.path.exists('~/.vim/ftplugin/python.vim'))

###############################################################################
############################## Modify_VIM_Prefs ###############################
###############################################################################

# TODO: FORREAL: Just take the VIM config and copy/paste whole crap instead of dicking around with regex of epic proportions

# TODO: Make generic function to find and uncomment lines in a list
#   - pathtofile, listoflines, comment character
# Lines to uncomment:
# TODO: need to make whole string work and sort out \n, \t etc
allow = ['if has\("autocmd"\)', 'filetype plugin indent on']
# Make sure pre dir exists
path = '/usr/share/vim/vimrc'
comment_char = '"'
if os.path.exists(path) == True:
    print('[+] \'' + path + '\' found. Modifying file!')
    lines_out = ''
    lines_in = '' # For debugging
    # do shit
    with open(path, 'r') as f:
        #TODO: iterate allow[:]
        target_pattern = re.compile(allow[0])
        for line in f:
            lines_in += line
            # TODO: replace with for loop
            match = re.search(target_pattern, line)
            
            if match:
                index = match.span()[0]
                if line[index-1] == comment_char:
                    line_out = line[1:]
            else:
                line_out = line
            
            lines_out += line_out
    f.closed
    
    # Write to file
    with open(path + 'test', 'w') as f:
        f.writelines(lines_out)
    f.closed
            
        
else:
    print('[-] WARNING: No /usr/share/vim/vimrc found. Settings will NOT take'+
        ' effect')
