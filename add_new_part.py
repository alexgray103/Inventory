from tkinter import *
import tkinter.font as TkFont

import pandas as pd
import csv
import os
import webbrowser

class new_part_window:
    def __init__(self, parent):
        self.new_part_var = 1
        self.parent = parent
        self.csv_location = '/Users/Alexander/Desktop/Inventory/LAB_BOM.csv'
        self.label_font = TkFont.Font(family="Helvetica", size=48, weight="bold", underline = True)
        self.small_label = TkFont.Font(family="Helvetica", size=36, weight="bold", underline = True)
        self.smaller_label = TkFont.Font(family="Helvetica", size=30, weight="bold", underline = True)
        self.inventory_font = TkFont.Font(family="Helvetica", size=26, weight="bold")
        self.smaller = TkFont.Font(family="Helvetica", size=25, weight="bold")
        
        self.df = pd.read_csv(self.csv_location)
        self.bg = 'gray14'
        self.lite_bg = 'gray60'
        self.text_color = 'gray4'
        
        
    def callback(event, url):
        try:
            webbrowser.open_new(url)
        except:
            pass
        
    def create_window(self, item_info):
        self.top = Toplevel(self.parent, bg = self.bg)
        self.top.attributes('-fullscreen', True)
        
        #label = Label(self.top, text = "need to add new part").grid(ro
        back_btn = Button(self.top, fg = 'red', text = 'Back',
                          width = 40, height = 4, command = self.top.destroy)
        back_btn.grid(row = 0 , column = 0, sticky = 'nw', padx = 15, pady = 5)
        
        name= Label(self.top, text = item_info[0], font = self.label_font, fg = 'white', bg = self.bg)
        name.grid(row = 1, column = 0, sticky = 'nw', padx = 15)
        
        
        info_frame = Frame(self.top, bg = self.lite_bg)
        info_frame.grid(row = 2, column = 0, sticky = 'nsew', padx = 20, pady = 10)
        
        
        #### Description required for device
        description_lbl  = Label(info_frame, text = 'Description: ', font = self.small_label,
                                 fg = self.text_color, bg = self.lite_bg , wraplength = 300)
        description_lbl.grid(row = 1, column = 0, sticky = 'nw', pady = (8,0))
        
        info = Label(info_frame, text = item_info[1], font = self.inventory_font, fg = self.text_color, bg = self.lite_bg )
        info.grid(row = 2, column = 0, sticky = 'nw')
          
        #### quantity required for device
        qty  = Label(info_frame, text = 'Quantity required for Device:', font = self.smaller_label, fg = self.text_color, bg = self.lite_bg )
        qty.grid(row = 3, column = 0, sticky = 'nw', pady = (10,0))
        
        info = Label(info_frame, text = item_info[3], font = self.inventory_font, fg = self.text_color, bg = self.lite_bg )
        info.grid(row = 4, column = 0, sticky = 'nw')
        
        #### vendor for part
        vendor  = Label(info_frame, text = 'Vendor:', font = self.smaller, fg = self.text_color, bg = self.lite_bg)
        vendor.grid(row = 1, column = 1, pady = (8,0), sticky = 'nw')
        
        info = Label(info_frame, text = item_info[2], font = self.smaller, fg = self.text_color, bg = self.lite_bg)
        info.grid(row = 1, column = 2, sticky = 'nw', pady = (8,0))
        
        #### hyperlink for part
        hyperlink = Label(info_frame, text = "Website Link", font = self.smaller_label, fg = 'cyan2', bg = self.lite_bg )
        hyperlink.grid(row = 7, column = 0, sticky = 'nw', pady = 10)
        hyperlink.bind("<Button-1>", lambda e: self.callback(item_info[7]))
        
        #### cost for part
        cost = Label(info_frame, text = "Cost:", font = self.smaller_label, fg = self.text_color, bg = self.lite_bg )
        cost.grid(row = 5, column = 0, sticky = 'nw', pady = (10,0))
        
        try:
            reduced_cost = float(item_info[6].strip('$'))/float(item_info[5])
            label_str = item_info[6] + ' ($' + str(reduced_cost) + '/unit)'
        except:
            label_str = item_info[6]
        
        
        
        number_cost = Label(info_frame, text = label_str, font = self.inventory_font, fg = self.text_color, bg = self.lite_bg )
        number_cost.grid(row = 6, column = 0, sticky = 'nw')
        
        #### number of components per device
        number  = Label(info_frame, text = 'Number of Components per Device:', font = self.smaller, fg = self.text_color, bg = self.lite_bg )
        number.grid(row = 8, column = 0, pady = (8,0), sticky = 'nw')
        
        try:
            reduced_cost = float(item_info[6].strip('$'))/float(item_info[5])
            total_cost = str(item_info[3]) + '  (Total Cost: $' + str(reduced_cost*int(item_info[3])) + ')'
        except:
            total_cost = item_info[3]
        number = Label(info_frame, text = total_cost, font = self.smaller, fg = self.text_color, bg = self.lite_bg )
        number.grid(row = 9, column = 0, sticky = 'nw', padx = 40)
        
    def toggle_fullscreen(self, _event):
        self.top.quit()
        self.top.destroy()