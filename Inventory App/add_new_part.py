from tkinter import *
import tkinter.font as TkFont

import pandas as pd
import csv
import os

class new_part_window:
    def __init__(self, parent):
        self.new_part_var = 1
        self.parent = parent
        
    def create_window(self):
        self.top = Toplevel(self.parent, bg = 'gray14')
        self.top.attributes('-fullscreen', True)
        
        #label = Label(self.top, text = "need to add new part").grid(ro
        back_btn = Button(self.top, fg = 'red', text = 'Back',
                          width = 40, height = 4, command = self.top.destroy)
        back_btn.grid(row = 0 , column = 0, sticky = 'ew')