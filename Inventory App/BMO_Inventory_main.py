from tkinter import *
import tkinter.font as TkFont

import pandas as pd
import csv
import os
from add_new_part import new_part_window

class inventory_main:
    def __init__(self, parent_frame):
        self.root = parent_frame
        self.fullscreen_handler = True
        self.helv72 = TkFont.Font(family="Helvetica", size=72, weight="bold")
        #self.label_font = TkFont.Font(family="Helvetica", size=36, weight="bold")
        self.label_font = TkFont.Font(family="Helvetica", size=36, weight="bold", underline = True)
        self.inventory_font = TkFont.Font(family="Helvetica", size=18, weight="bold")
        self.small_font = TkFont.Font(family="Helvetica", size=18, weight="bold")
        self.title_small_font = TkFont.Font(family="Helvetica", size=24, weight="bold", underline = True)
        
        
        self.background_color = "gray60"
        self.dark_background = 'gray35'
        
        self.csv_location = '/Users/Alexander/Desktop/Inventory/LAB_BOM.csv'
        
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.root.title("BMO Lab Inventory")
        self.root.attributes('-fullscreen', self.fullscreen_handler) # fullscreen on touchscreen
        self.root.configure(bg= self.background_color)
        self.root.minsize(800,480)
        
        ### create a data frame for the inventory
        self.df = pd.read_csv(self.csv_location)
        self.bom_df = []
        
        #low inventory list
        self.inventory_low = []
        
        ### allow for new part window
        self.new_part = new_part_window(root)
        
        ########## Scrollable page ############################
        #######################################################

        # Create A Main Frame
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=1)

        # Create A Canvas
        self.my_canvas = Canvas(self.main_frame, bg = self.background_color)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar To The Canvas
        self.my_scrollbar = Scrollbar(self.main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)


        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all")))
        self.my_canvas.bind_all("<Down>",  lambda event: self.my_canvas.yview_scroll(-1, "units"))
        self.my_canvas.bind_all("<Up>", lambda event: self.my_canvas.yview_scroll(1, "units"))
        self.my_canvas.bind_all("<MouseWheel>", lambda event: self.my_canvas.yview_scroll(-1*event.delta, "units"))
        
        # Create ANOTHER Frame INSIDE the Canvas
        self.second_frame = Frame(self.my_canvas, bg = self.background_color)
        
        self.my_canvas.focus_set()
       
       # Add that New frame To a Window In The Canvas
        self.my_canvas.create_window((0,0), window=self.second_frame, anchor="nw")
        
        label_title = Label(self.second_frame, fg = 'white', bg = self.background_color,
                            text = 'BMO lab Inventory', font = self.helv72)
        label_title.grid(row = 0, column = 0, columnspan = 3, padx = 50, pady = 10, sticky = 'nsew')
        
        #sort data frame
        self.df.sort_values(by = 'Part')
        
        #paint the screen with inventory details
        self.inventory_update()
        
        #self.root.after(4000, self.inventory_check)
        #self.inventory_check()
        
        create_bom_btn = Button(self.second_frame, text = 'Create BOM', height = 7, command = self.create_bom)
        create_bom_btn.grid(row =1, column = 0, padx = 5, pady = 4, sticky = 'nsew')
        
        new_part = Button(self.second_frame, text = "Add New Device",
                           command = self.inventory_check, height = 7)
        new_part.grid(row =1, column = 1, columnspan = 2, padx = 5, pady = 4, sticky = 'nsew')
        
    def inventory_check(self):
        self.inventory_popup = Toplevel(self.root, bg = self.background_color)
        self.inventory_popup.geometry('1000x800')
        self.inventory_popup.title('Inventory Status')
        self.inventory_popup.lift()
                
        title = Label(self.inventory_popup, text = "The following Items need to be Restocked",
                      bg = self.background_color, fg = 'white', font = self.title_small_font)
        title.grid(row = 0, column = 0, padx = 10)
        c = 0
        r = 1
        last_row = 23
        needed = list(range(250))
        x = 0
        
        for value in self.inventory_low:
            needed[value] = 0
            RQ = self.df.iloc[value, 3]
            information = self.df.iloc[value, 8]
            needed[value] += int(RQ - information)
            low = '-' + str(self.df.iloc[value,0]) + '(qty: ' + str(needed[value]) + ')'
            label = Label(self.inventory_popup, text = low, font = self.small_font,
                          fg = 'white', bg = self.background_color, wraplength = 400)
            label.grid(row = r, column = c, sticky = 'nw', padx = 10)
            r+=1
            
            if x ==15:
                c += 1
                r = 1
            x+= 1
            
        ok_button = Button(self.inventory_popup, text = "OK",
                           command = self.inventory_popup.destroy, width = 40, height = 5)
        ok_button.grid(row = last_row+1, column = 0, pady  =2, sticky = 'nsew')
                
        create_inventory_bom = Button(self.inventory_popup, text = 'Create BOM',
                                      width = 40, height = 5, command = self.create_bom)
        create_inventory_bom.grid(row = last_row+1, column = 1, pady = 2, padx = 1, sticky = 'nsew')
        
        self.root.after(10000, self.inventory_popup.destroy)
            
        
    def create_bom(self):
        # create window to paste 
        self.bom = Toplevel(self.root, bg = self.background_color)
        self.bom.geometry('1000x800')
        self.bom.title('Bill of Materials')
        self.bom.lift()
        title = Label(self.bom, text = "The following items were added to your BOM:",
                      bg = self.background_color, fg = 'white', font = self.title_small_font)
        title.grid(row = 0, column = 0, padx = 10)
        
        BOM_path = '/Users/Alexander/Desktop/Inventory'
        needed = list(range(self.row))
        # get the important information
        new_df = self.df.iloc[self.inventory_low, [0,1,2,7]]
        
        c = 0
        r = 1
        last_row = 23
        
        for info in self.inventory_low:
            
            RQ = self.df.iloc[info, 3]
            information = self.df.iloc[info, 8]
            needed[info] += int(3*RQ - information)
            low = '-' + str(self.df.iloc[info,0]) + ' (qty: ' + str(needed[info]) + ')'
            label = Label(self.bom, text = low, font = self.small_font,
                          fg = 'white', bg = self.background_color, wraplength = 400)
            label.grid(row = r, column = c, sticky = 'nw', padx = 10)
            r+=1
            
            if info ==20:
                c += 1
                r = 1
        qty = pd.DataFrame(needed)
        
        
        new_df['Qty'] = qty
        
        columns_titles = ["Part", "Description", "Vendor", "Qty","link"]
        new_df=new_df.reindex(columns=columns_titles)
        self.save_file = '/Users/Alexander/Desktop/Inventory/bom.csv'
        new_df.to_csv(self.save_file, mode = 'w', index=False)
        
            
        
        ok_button = Button(self.bom, text = "OK",
                           command = self.bom.destroy, width = 40, height = 5)
        ok_button.grid(row = last_row+1, column = 0, columnspan = 2, pady  =2)
        
        
        self.root.after(20000, self.bom.destroy)
        
    def toggle_fullscreen(self, _event):
        self.fullscreen_handler = not self.fullscreen_handler
        self.root.attributes('-fullscreen', self.fullscreen_handler)
        self.root.quit()
        self.root.destroy()
        
    def inventory_update(self):
        ### allow up to 250 elements in the inventorys
        self.inventory_frame = list(range(250))
        self.item_number_lbl = list(range(250))
        self.item_btn = list(range(250))
        self.plus_button = list(range(250))
        self.minus_button = list(range(250))
        self.item_name = list(range(250))
        self.row = len(self.df.index)
        
        r = 2
        c = 0
        button_width = 7
        padding = 5
        button_height = 1
        for x in range(self.row):
            inventory_row = self.df.iloc[x, :]
            self.item_name[x] = inventory_row
            
            self.inventory_frame[x] = Frame(self.second_frame, bg = 'green')
            
            self.inventory_frame[x].grid(row = r, column = c, padx = padding, pady = 3)
            
            # create label for item
            self.item_btn[x] = Button(self.inventory_frame[x], text = inventory_row[0], font = self.inventory_font,
                                fg = 'black', bg='#54FA9B', width = 15, height = 2, wraplength = 150, command = lambda x=x: self.new_part.create_window(self.item_name[x]))
            self.item_btn[x].grid(row = 0, column = 0, pady = 1, padx = 1, ipadx = 5, sticky = 'nsew')
            
            self.item_number_lbl[x] = Label(self.inventory_frame[x], text = inventory_row[8], font = self.inventory_font,
                               bg = self.dark_background, fg = 'white', width = button_width , height = 1)
            self.item_number_lbl[x].grid(row = 0, column = 2, ipady = 1, pady = 1, padx = 1, ipadx = 5, sticky = 'nsew')
            
            self.plus_button[x] = Button(self.inventory_frame[x], text = '+', font = self.inventory_font,
                               bg = self.dark_background, width = button_width , height = 1, command = lambda x=x: self.increase_value(x))
            self.plus_button[x].grid(row = 0, column = 3, ipady = 1, pady = 1, padx = 1, ipadx = 5, sticky = 'nsew')
            
            self.minus_button[x] = Button(self.inventory_frame[x], text = '-', font = self.inventory_font,
                               bg = self.dark_background, width = button_width , height = 3, command = lambda x=x: self.decrease_value(x))
            self.minus_button[x].grid(row = 0, column = 1, ipady = 1, pady = 1, padx = 1, ipadx = 5, sticky = 'nsew')
            self.inventory_needed = []
            self.inventory_low = []
            
            if int(inventory_row[8]) < int(inventory_row[3]):
                self.inventory_frame[x].configure(bg = 'indianred1')
                #get the row number that has a low inventory and save to a string
                self.inventory_low += [x]
            elif int(inventory_row[8]) >= int(inventory_row[3]) and int(inventory_row[8]) < int(3*inventory_row[3]):
                self.inventory_frame[x].configure(bg = 'yellow')
                self.inventory_needed += [x]
            else:
                self.inventory_frame[x].configure(bg = 'green')
                
            c+=1
            if c > 2:
                c = 0
                r +=1
            
    def increase_value(self, x):
        inventory_row = self.df.iloc[x, 8]+1
        self.item_number_lbl[x].configure(text = str(inventory_row))
        self.df.iloc[x,8] = inventory_row
        self.check_page()
        
    def decrease_value(self, x):
        
        inventory_row = self.df.iloc[x, 8]
        
        if inventory_row > 0:
            self.item_number_lbl[x].configure(text = str(inventory_row-1))
            self.df.iloc[x,8] = inventory_row-1
        self.check_page()
            
    def check_page(self):
        self.inventory_low = []
        for x in range(self.row):
            inventory_row = self.df.iloc[x, :]
            self.inventory_needed = []
            if int(inventory_row[8]) < int(int(inventory_row[3])):
                self.inventory_frame[x].configure(bg = 'indianred1')
                #get the row number that has a low inventory and save to a string
                self.inventory_low += [x]
            elif int(inventory_row[8]) >= int(inventory_row[3]) and int(inventory_row[8]) < int(3*inventory_row[3]):
                self.inventory_frame[x].configure(bg = 'yellow')
                self.inventory_needed += [x]
            else:
                self.inventory_frame[x].configure(bg = 'green')
        
        
root = Tk()
app = inventory_main(root)

if __name__ == "__main__":
    root.mainloop()
