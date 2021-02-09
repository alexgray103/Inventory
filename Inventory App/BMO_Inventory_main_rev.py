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
        self.small_font = TkFont.Font(family="Helvetica", size=15, weight="bold")
        self.title_small_font = TkFont.Font(family="Helvetica", size=24, weight="bold", underline = True)
        
        
        self.background_color = "gray60"
        self.dark_background = 'gray35'
        try:
            self.csv_location = '/Users/Alexander/Desktop/Inventory/LAB_BOM.csv'
        except:
            self.csv_location = '/Users/Alexander/Desktop/Inventory/LAB_BOM.csv'
            
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.root.title("BMO Lab Inventory")
        self.root.attributes('-fullscreen', self.fullscreen_handler) # fullscreen on touchscreen
        self.root.configure(bg= self.background_color)
        self.root.minsize(800,480)
        
        
        ### create a data frame for the inventory
        self.df = pd.read_csv(self.csv_location)
        #alphabetize the dataframe for easy viewing 
        self.df = self.df.sort_values(self.df.columns[0])
        
        self.bom_df = []
        
        #low inventory list
        self.inventory_low = []
        self.inventory_needed = []
        
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
        self.my_canvas.bind_all("<Down>",  lambda event: self.my_canvas.yview_scroll(1, "units"))
        self.my_canvas.bind_all("<Up>", lambda event: self.my_canvas.yview_scroll(-1, "units"))
        self.my_canvas.bind_all("<Button-4>", lambda event: self.my_canvas.yview_scroll(-1, "units"))
        self.my_canvas.bind_all("<Button-5>", lambda event: self.my_canvas.yview_scroll(1, "units"))
        
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
        create_bom_btn.grid(row =1, column = 0, padx = 10, pady = 4, sticky = 'nsew')
        
        new_part = Button(self.second_frame, text = "Add New Device",
                           command = self.inventory_check, height = 7)
        new_part.grid(row =1, column = 1, columnspan = 2, padx = 10, pady = 4, sticky = 'nsew')
        
    def center_window(self, popup):
        screen_width = self.root.winfo_screenheight()
        screen_height = self.root.winfo_screenwidth()
        
        size = tuple(int(_) for _ in popup.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2 
        y = screen_height/2 - size[1]/2
        
        popup.geometry("+%d+%d" % (300, 300))
            
    def inventory_check(self):
        self.inventory_popup = Toplevel(self.root, bg = self.background_color)
        self.inventory_popup.title('Inventory Status')
        self.inventory_popup.lift()
        
        self.center_window(self.inventory_popup)
        def destroy_popup():
            self.inventory_popup.destroy()
            
        
        c = 0
        r = 1
        last_row = 0
        needed = list(range(self.row))
        for x in range(self.row):
            needed[x] = 0
        # get the important information
        
        c = 0
        r = 1
        last_row = 23
        x = 0
        
        if not self.inventory_needed:
            title = Label(self.inventory_popup, text = "Your all set to build a new device!!!",
                      bg = self.background_color, fg = 'white', font = self.title_small_font)
            title.grid(row = 0, column = 0, pady = 50, padx = 50)
        else:
            for info in self.inventory_needed:
                
                RQ = self.df.iloc[info, 3]
                information = self.df.iloc[info, 8]
                needed[info] += int(RQ - information)
                
                low = '-' + str(self.df.iloc[info,0]) + ' (qty: ' + str(needed[info]) + ')'
                label = Label(self.inventory_popup, text = low, font = self.small_font,
                              fg = 'white', bg = self.background_color, wraplength = 500)
                label.grid(row = r, column = c, sticky = 'nw', padx = 20)
                r+=1
                
                if x ==15:
                    c += 1
                    r = 1
                x+=1
            
                title = Label(self.inventory_popup, text = "The following are needed to create device: ",
                          bg = self.background_color, fg = 'white', font = self.title_small_font)
                title.grid(row = 0, column = 0, columnspan = c+1, padx = 10)
                
                create_inventory_bom = Button(self.inventory_popup, text = 'Create BOM',
                                          width = 40, height = 5, command = self.create_bom)
                
                create_inventory_bom.grid(row = last_row+1, column = 1, pady = 5, padx = 5, sticky = 'nsew')
        ok_button = Button(self.inventory_popup, text = "OK",
                               command = destroy_popup, width = 40, height = 5)
        ok_button.grid(row = last_row+1, column = 0, pady  =5, padx = 5, sticky = 'nsew')
                    
        
            
        self.root.after(10000, self.inventory_popup.destroy)
                
            # cofngiure resizing of buttons
        
    
        
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
            needed[info] = int(2*RQ - information)
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
        #self.save_file = '/home/pi/Documents/Inventory-main/Inventory_App/bom.csv'
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
        
    def return_needed_val(self, the_list, val):
        return [value for value in the_list if value !=val]    
    
    def inventory_update(self):
        ### allow up to 250 elements in the inventorys
        self.inventory_frame = list(range(250))
        self.item_number_lbl = list(range(250))
        self.item_btn = list(range(250))
        self.plus_button = list(range(250))
        self.minus_button = list(range(250))
        self.item_info = list(range(250))
    
        self.row = len(self.df.index)
        
        r = 1
        c = 0
        button_width = 4
        padding = 12
        button_height = 1
        
        internal = 4
        self.inventory_needed = []
        
        ### list for types of components
        self.type_list = []
        self.type = []
        
        #handler to build the type frames
        build_type = True
        for loc in range(self.row):
            inventory_row = self.df.iloc[loc, :]
            self.item_info[loc] = inventory_row
            
            self.type =  inventory_row[9]
            ### create item type frame
            if self.type not in self.type_list:
                self.type_list += [self.type]
        
        self.type_frame = list(range(len(self.type_list)))
        
        ### handle column and row stuff for each type
        self.row_handler = [1]*len(self.type_list)
        self.col_handler = [0]*len(self.type_list)
        
        
        for x in range(self.row):
            inventory_row = self.df.iloc[x, :]
            self.item_info[x] = inventory_row
            
            self.type =  inventory_row[9]
            
            
            
            if build_type:
                item = 0
                for item_type in self.type_list:
                    self.type_frame[item] = Frame(self.second_frame, bg = 'gray80')
                    self.type_frame[item].grid(row = item+2, column = 0, columnspan = 2, padx = padding, pady = 5)
                    
                    type_label = Label(self.type_frame[item], font = self.label_font,
                                       bg = 'gray80', text = item_type)
                    type_label.grid(row = 0, column = 1,  sticky = 'nsew')
                    item+=1
                build_type = False
            
            item_type_handler = self.type_list.index(self.type)
            
            self.inventory_frame[x] = Frame(self.type_frame[item_type_handler], bg = 'green')
            self.inventory_frame[x].grid(row = self.row_handler[item_type_handler], column = self.col_handler[item_type_handler], padx = padding, pady = 3)
            

            # create label for item
            self.item_btn = Button(self.inventory_frame[x], text = inventory_row[0], font = self.inventory_font,
                                fg = 'black', bg='#54FA9B', width = 15, height = 2, wraplength = 175,
                                   command = lambda x=x: self.new_part.create_window(self.item_info[x]))
            self.item_btn.grid(row = 0, column = 0, pady = internal, padx = internal, ipadx = 2, sticky = 'nsew')
            
            self.item_number_lbl[x] = Label(self.inventory_frame[x], text = inventory_row[8], font = self.inventory_font,
                               bg = self.dark_background, fg = 'white', width = button_width , height = 1)
            self.item_number_lbl[x].grid(row = 0, column = 2, ipady = 1,
                                         pady = internal, padx = 1, ipadx = 5, sticky = 'nsew')
            
            self.plus_button[x] = Button(self.inventory_frame[x], text = '+', font = self.inventory_font,
                               bg = self.dark_background, width = button_width , height = 1, command = lambda x=x: self.increase_value(x))
            self.plus_button[x].grid(row = 0, column = 3, ipady = 1, pady = internal, padx = internal, ipadx = 5, sticky = 'nsew')
            
            self.minus_button[x] = Button(self.inventory_frame[x], text = '-', font = self.inventory_font,
                               bg = self.dark_background, width = button_width , height = 3, command = lambda x=x: self.decrease_value(x))
            self.minus_button[x].grid(row = 0, column = 1, ipady = 1, pady = internal, padx = 1, ipadx = 5, sticky = 'nsew')
            
            
            
            if int(inventory_row[8]) < int(2*int(inventory_row[3])) and int(inventory_row[8]) >= int(inventory_row[3]):
                self.inventory_frame[x].configure(bg = 'yellow')
                
                self._inventory_needed = self.return_needed_val(self.inventory_needed, x)
                #get the row number that has a low inventory and save to a string
                self.inventory_low += [x]
                
            if int(inventory_row[8]) < int(inventory_row[3]):
                self.inventory_frame[x].configure(bg = 'indianred1')
                self.inventory_needed += [x]
            
            self.col_handler[item_type_handler]+= 1
            if self.col_handler[item_type_handler] > 2:
                self.col_handler[item_type_handler] = 0
                self.row_handler[item_type_handler] += 1
            
    def increase_value(self, x):
        inventory_row = self.df.iloc[x, 8]+1
        self.item_number_lbl[x].configure(text = str(inventory_row))
        self.df.iloc[x,8] = inventory_row
        self.check_page()
        self.df.to_csv(self.csv_location, mode = 'w', index=False)
        
    def decrease_value(self, x):
        
        inventory_row = self.df.iloc[x, 8]
        
        if inventory_row > 0:
            self.item_number_lbl[x].configure(text = str(inventory_row-1))
            self.df.iloc[x,8] = inventory_row-1
        self.check_page()
        self.df.to_csv(self.csv_location, mode = 'w', index=False)
        
        
    def check_page(self):
        self.inventory_low = []
        self.inventory_needed = []
        for x in range(self.row):
            inventory_row = self.df.iloc[x, :]
            
            if  int(inventory_row[8]) < int(2*int(inventory_row[3])) and int(inventory_row[8]) >= int(inventory_row[3]):
                self.inventory_frame[x].configure(bg = 'yellow')
                self._inventory_needed = self.return_needed_val(self.inventory_needed, x)
                #get the row number that has a low inventory and save to a string
                self.inventory_low += [x]
            elif int(inventory_row[8]) < int(inventory_row[3]):
                self.inventory_frame[x].configure(bg = 'indianred1')
                self.inventory_needed += [x]
            else:
                self.inventory_frame[x].configure(bg = 'green')
                self._inventory_needed = self.return_needed_val(self.inventory_needed, x)
        
        
        
root = Tk()
app = inventory_main(root)

if __name__ == "__main__":
    root.mainloop()
