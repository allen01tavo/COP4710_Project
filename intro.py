'''
Created on Jun 29, 2016

@author: gmaturan
'''

import Tkinter as Tk

import time as t

class intro:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.intro_window = Tk.Tk('Intro')
        self.intro_window.minsize(width=666, height=380)
        
    def flash_screen(self):
        path = 'main_logo.png'
        
        print(path)
