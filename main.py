# PO update query string

#from typing import Any
from tkinter import END
import customtkinter
import vbstringbuilder
# main applicaiton
class App(customtkinter.CTk):
	"""
	Creates the main application window
	"""
	# define the applicaiton. Includes classes and task
	def __init__(self):
		
		super().__init__()
		self._set_appearance_mode("System")
		self.geometry("1024x768")
		self.title("KV_SCDS")
		
		# create the input frame
		self.current_kv_frame = CurrentInputFrame(master=self)
		self.current_kv_frame.grid(row=0,column=0,sticky="nswe")
		self.current_kv_frame.configure(border_width=3)

		# create the change data frame
		self.change_data_frame = ChangeDataFrame(master=self)
		self.change_data_frame.grid(row=0,column=1,sticky="nswe")
		self.change_data_frame.configure(border_width=3)

		# create the output frame
		self.output_kv_frame = OutputStringFrame(master=self)
		self.output_kv_frame.grid(row=1,column=0,sticky="we")

		# create the 'do' button
		self.proc_button = customtkinter.CTkButton(self, text="Transform",command=self.do_work)
		self.proc_button.grid(row=5,column=0)

	def do_work(self):
		"""
		Work is done here.

		First we clearn up the display boxes.
		Second create dictionarys, format strings and assign to values.
		Finally push data to be displayed into approate areas.
		"""
		self.change_data_frame.bna_data.delete(1.0,END) #clean up the What's Changed section
		self.change_data_frame.removed_data.delete(1.0,END) #clean up the What's Removed section
		self.change_data_frame.added_data.delete(1.0,END) #clean up the What's Added section


		current_dict = vbstringbuilder.dict_csv(self.current_kv_frame.current_item_string.get().split(","),self.current_kv_frame.current_value_string.get().split(",")) #build a dictionary from csv strings
		new_dict = vbstringbuilder.dict_line(self.current_kv_frame.new_items_textbox.get(1.0,END).splitlines(),self.current_kv_frame.new_values_textbox.get(1.0,END).splitlines()) #build a dictionary from line items
		keys_with_values, removed_keys = vbstringbuilder.remove_empties(new_dict) #sort values and return a dictioanry and list
		items_added = vbstringbuilder.added_items(current_dict,new_dict) #items that were added
		item_string = vbstringbuilder.list_of_string(keys_with_values.keys()) #build string with double quoted csv values
		value_string = vbstringbuilder.list_of_number(keys_with_values.values()) #build string with csv values

		self.change_data_frame.bna_data.insert(1.0,vbstringbuilder.bna_data(current_dict,new_dict)) #update What's Changed
		self.change_data_frame.removed_data.insert(1.0,"\n".join([key for key in removed_keys])) #update What's Removed
		self.change_data_frame.added_data.insert(1.0,"\n".join([key for key in items_added])) #update What's added
		self.output_kv_frame.new_items.set(item_string) #update key string
		self.output_kv_frame.new_values.set(value_string) #update value string

# input frame
class CurrentInputFrame(customtkinter.CTkFrame):

	def __init__(self, master):		
		super().__init__(master)
		# labels for input string
		self.label_cur_items = customtkinter.CTkLabel(self,text="Current Item String")
		self.label_cur_items.grid(row=0,column=0,padx=5,pady=5,ipadx=5,ipady=5)
		self.label_cur_prices = customtkinter.CTkLabel(self,text="Current Price String")
		self.label_cur_prices.grid(row=1,column=0,padx=5,pady=5,ipadx=5,ipady=5)
		self.label_new_items = customtkinter.CTkLabel(self,text="New Item String")
		self.label_new_items.grid(row=2,column=0,padx=5,pady=5,ipadx=5,ipady=5)
		self.label_new_prices = customtkinter.CTkLabel(self,text="New Price String")
		self.label_new_prices.grid(row=3,column=0,padx=5,pady=5,ipadx=5,ipady=5)

		# current item string entry box
		self.current_item_string = customtkinter.CTkEntry(self,width=350)
		self.current_item_string.grid(row=0,column=1,padx=5,pady=5,ipadx=5,ipady=5)
		# current value string entry box				
		self.current_value_string = customtkinter.CTkEntry(self,width=350)
		self.current_value_string.grid(row=1,column=1,padx=5,pady=5,ipadx=5,ipady=5)
		# new item string text box
		self.new_items_textbox = customtkinter.CTkTextbox(master=self,width=350)
		self.new_items_textbox.grid(row=2,column=1,padx=5,pady=5,ipadx=5,ipady=5)
		# new value string text box
		self.new_values_textbox = customtkinter.CTkTextbox(master=self,width=350)
		self.new_values_textbox.grid(row=3,column=1,padx=5,pady=5,ipadx=5,ipady=5)

# show changes being made from old to new
class ChangeDataFrame(customtkinter.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		# labels for change boxes.
		self.label_bna = customtkinter.CTkLabel(self,text="What's Changed")
		self.label_bna.grid(row=0,column=0,padx=5,pady=5,ipadx=5,ipady=5)
		self.label_added = customtkinter.CTkLabel(self,text="What's New")
		self.label_added.grid(row=1,column=0,padx=5,pady=5,ipadx=5,ipady=5)
		self.label_removed = customtkinter.CTkLabel(self,text="What's Gone")
		self.label_removed.grid(row=2,column=0,padx=5,pady=5,ipadx=5,ipady=5)
		
		# boxes for change boxes
		self.bna_data = customtkinter.CTkTextbox(self,height=175,width=350)
		self.bna_data.grid(row=0,column=1,padx=5,pady=5,ipadx=5,ipady=5)
		self.added_data = customtkinter.CTkTextbox(self,height=175,width=350)
		self.added_data.grid(row=1,column=1,padx=5,pady=5,ipadx=5,ipady=5)
		self.removed_data = customtkinter.CTkTextbox(self,height=175,width=350)
		self.removed_data.grid(row=2,column=1,padx=5,pady=5,ipadx=5,ipady=5)
# output change frame
class OutputStringFrame(customtkinter.CTkFrame):

	def __init__(self, master):		
		super().__init__(master)
		# new strings for items and price
		self.label_new_items = customtkinter.CTkLabel(self,text="Key String Out")
		self.label_new_items.grid(row=0,column=0,padx=5,pady=5,ipadx=5,ipady=5)
		self.label_new_prices = customtkinter.CTkLabel(self,text="Value String Out")
		self.label_new_prices.grid(row=1,column=0,padx=5,pady=5,ipadx=5,ipady=5)
		# item string entry box
		self.new_items = customtkinter.StringVar(self)
		self.new_item_string = customtkinter.CTkEntry(self,textvariable=self.new_items,width=350)
		self.new_item_string.grid(row=0,column=1,columnspan=3,padx=5,pady=5,ipadx=5,ipady=5)
		#self.new_item_string.configure(self,width=new_items_width)
		# value string entry box			
		self.new_values = customtkinter.StringVar(self)	
		self.new_value_string = customtkinter.CTkEntry(self,textvariable=self.new_values,width=350)
		self.new_value_string.grid(row=1,column=1,columnspan=3,padx=5,pady=5,ipadx=5,ipady=5)


# run app
app = App()
app.mainloop()
