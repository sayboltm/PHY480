#!/usr/bin/env python
#####################
# '''setup_vim.py'''
# Desc: A program to setup VIM bc so many linux
# V 1.0 Beta
# 2/9/17

# VIM IS ALREADY SETUP for leetness on Ubuntu. TO BE CONTINUED.

import os

# Preferences to write to 'python.vim':
preferences = 'set tabstop=8\nset expandtab\nset shiftwidth=4\nset softtabstop=4'
filename = 'python.vim'

print('~/.vim exists: ' + str(os.path.isdir('~/.vim')))
if os.path.isdir('~/.vim') == False:
    print('above is false')
    #os.mkdir('~/.vim')
    os.makedirs('~/.vim')
else:
    print('Dir has been made!')

if os.path.isdir('~/.vim/ftplugin') == False:
    print('[-] \'~/.vim/ftplugin\' DNE. Creating....')
    os.makedirs('~/.vim/ftplugin')
else:
    print('Dir2 has been made!')

if os.path.exists('~/.vim/ftplugin/python.vim') == False:
    print('[-] Config file not found. Creating....')
    os.chdir('~/.vim/ftplugin/')
    with open(filename, 'w') as f:
        f.writelines(preferences)
    f.closed
else:
    print('File already exist')

print(os.path.isdir('~/.vim/ftpugin'))
print(os.path.exists('~/.vim/'))
print(os.path.isdir('~/.vim/'))
print(os.path.exists('~/.vim/ftplugin/python.vim'))
