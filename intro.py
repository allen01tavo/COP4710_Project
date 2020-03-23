'''
Created on Jun 29, 2016

@author: gmaturan
'''

import tkinter as Tk
import os

import time as t
#from _curses import flash



class intro():


    def __init__(self):
        '''
        conform
        
        '''

    def flash_screen(self):
        root = Tk.Tk()
        # show no frame
        root.overrideredirect(True)
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.geometry('%dx%d+%d+%d' % (width*0.8, height*0.8, width*0.1, height*0.1))
        # take a .jpg picture you like, add text with a program like PhotoFiltre
        # (free from http://www.photofiltre.com) and save as a .gif image file
        image_file = 'main_logo.png'
        #assert os.path.exists(image_file)
        # use Tkinter's PhotoImage for .gif files
        self.lable = Tk.Label(root, fg = 'blue', bg = "blue", text = '')
        self.lable.pack(side = 'top')
        print(os.path.exists(image_file), "hola this")
        #This must be deleted
        image = Tk.PhotoImage(image_file)
        canvas = Tk.Canvas(root, height=height*1, width=width*1, bg="gray")
        canvas.create_image(width*0.8/2, height*0.8/2, image=image)
        canvas.pack()
        # show the splash screen for 5000 milliseconds then destroy
        root.after(10000, root.destroy)
        root.mainloop()
        

