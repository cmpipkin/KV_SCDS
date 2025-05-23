# PO update query string

from tkinter import END
from typing import Any
import customtkinter

# main applicaiton
class App(customtkinter.CTk):
	
	# define the applicaiton. Includes classes and task
	def __init__(self):
		
		super().__init__()
		self._set_appearance_mode("System")
		self.geometry("1024x768")
		self.title("Update PO report strings")
		
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
		self.proc_button = customtkinter.CTkButton(self, text="Transform",command=self.do_conversion)
		self.proc_button.grid(row=5,column=0)

	# working definitions
	# create a dictionay from current item and value strings
	def build_current_dict(self,keys,values):
		current_dict = {}
		if len(keys) != len(values):
			print(f"Number of items and prices are not equal")
			print(f"Key count: {len(keys)}")
			print(f"Value count: {len(values)}")
			return -1
		else:
			for i in range(len(keys)):
				current_dict.setdefault(keys[i].replace('"', ''),values[i])
		return current_dict
	# create a dictionay from spreedsheet columns
	def build_new_dict(self,keys,values):
		new_dict = {}
		if len(keys) != len(values):
			print(f"Number of items and prices are not equal")
			print(f"Key count: {len(keys)}")
			print(f"Value count: {len(values)}")
			return -1
		else:
			for i in range(len(keys)):
				if keys[i] != '':
					new_dict.setdefault(keys[i],values[i])
		return new_dict
	# show what values are changing
	def dict_bna(self,cur_dict,new_dict):
		bna = '\n'.join(f"{i}: {cur_dict.get(i)} -> {new_dict.get(i)}" for i in cur_dict.keys())
		self.change_data_frame.bna_data.delete(1.0,END)
		self.change_data_frame.bna_data.insert(1.0,bna)
	# change the values and report what keys no longer had a value
	def value_change(self,cur_dict,new_dict):
		working_dict = {}
		self.change_data_frame.removed_data.delete(1.0,END)
		for key in cur_dict.keys():
			if new_dict.get(key) != '':
				working_dict.setdefault(key,new_dict.get(key))
			else:
				# send empty values to What's Gone
				self.change_data_frame.removed_data.insert(1.0,f"{key} was removed\n")

		return working_dict
	# add items not in the current item string from spreedsheet
	def add_new_items(self,cur_dict,new_dict,final_dict):
		self.change_data_frame.added_data.delete(1.0,END)
		if len(new_dict.keys()) > len(cur_dict.keys()):
			for key in (set(list(new_dict.keys())) - set(list(cur_dict.keys()))):
				final_dict.setdefault(key,new_dict.get(key))
				# send added to What's New
				self.change_data_frame.added_data.insert(1.0,f"{key} was added\n")
		return final_dict
	# create item replacement string for PO report
	def item_string(self,keys):
		string = ','.join(['"'+i+'"' for i in list(keys)])
		return string
	# create value replacement string for PO report
	def value_string(self,values):
		string = ','.join([i for i in list(values)])
		return string
	# The work
	def do_conversion(self):
		current_dict = self.build_current_dict(self.current_kv_frame.get()[0].split(","),self.current_kv_frame.get()[1].split(","))
		new_dict = self.build_new_dict(self.current_kv_frame.get()[2].splitlines(),self.current_kv_frame.get()[3].splitlines())
		self.dict_bna(current_dict,new_dict)
		working_dict = self.value_change(current_dict,new_dict)
		final_dict = self.add_new_items(current_dict,new_dict,working_dict)
		self.output_kv_frame.new_items.set(self.item_string(final_dict.keys()))
		self.output_kv_frame.new_values.set(self.value_string(final_dict.values()))
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
# gather text box string data
	def get(self):
		string_data = []
		if self.current_item_string.get() != '':
			string_data.append(self.current_item_string.get())
		else:
			print(f"{self.label_cur_items.cget("text")} is emplty")

		if self.current_value_string.get() != '':
			string_data.append(self.current_value_string.get())
		else:
			print(f"{self.label_cur_prices.cget("text")} is empty")

		if self.new_items_textbox.get("1.0","end") != '':
			string_data.append(self.new_items_textbox.get("1.0","end"))
		else:
			print(f"{self.label_new_items.cget("text")} is empty")

		if self.new_values_textbox.get("1.0","end") != '':
			string_data.append(self.new_values_textbox.get("1.0","end"))
		else:
			print(f"{self.label_new_prices.cget("text")} is empty")
		return string_data
# show changes being made from old to new
class ChangeDataFrame(customtkinter.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		# labels for change boxes.
		self.label_bna = customtkinter.CTkLabel(self,text="Before and After")
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
		self.label_new_items = customtkinter.CTkLabel(self,text="New Item String")
		self.label_new_items.grid(row=0,column=0,padx=5,pady=5,ipadx=5,ipady=5)
		self.label_new_prices = customtkinter.CTkLabel(self,text="New Price String")
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
