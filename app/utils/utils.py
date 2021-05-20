import time

def is_number_correct(element, length, msg_keyword):
		
	input_str: str = element
	ret = len(input_str) == length and input_str.isdecimal()
	if ret:
		# element.configure(background='pale green')
		pass
	else:
		# element.configure(background='salmon')
		# messagebox.showwarning(
		# 	f'Incorrect format of {msg_keyword}',
		# 	f'Please enter a {length}-digit {msg_keyword}'
		# )
		print(
			f'Incorrect format of {msg_keyword}',
			f'Please enter a {length}-digit {msg_keyword}'
		)
		
	return ret

def log(addition, level='TEST'):#='DEBUG'):

	if (level == 'DEBUG'):
		return

	time_str = str(time.strftime("%d-%m-%Y %I:%M:%S %p", time.localtime()))
	# self.text_output.insert(tk.END, f'\n{time_str} | {addition}')
	# self.text_output.see(tk.END)
	print(f'\n{time_str} | {addition}')

def is_names_correct(names_list: list):

	if names_list:
		print_str = "\n".join(names_list)
		# messagebox.showinfo(title='Entered names', 
		# 	message=f'The entered names should have exact names registered on Cowin:\n {print_str}'
		# )
		print('Entered names\n', 
			f'The entered names should have exact names registered on Cowin:\n {print_str}'
		)

def get_age(birth_year: int) -> int:

	return 2021-int(birth_year)-1
