import time

def is_number_correct(self, element, length, msg_keyword):
	
	input_str: str = element.get()
	ret = len(input_str) == length and input_str.isdecimal()
	if ret:
		element.configure(background='pale green')
	else:
		element.configure(background='salmon')
		messagebox.showwarning(
			f'Incorrect format of {msg_keyword}',
			f'Please enter a {length}-digit {msg_keyword}'
		)
	return ret

def log_fn(self, addition, level='DEBUG'):

	if (level == 'DEBUG'):
		return

	time_str = str(time.strftime("%d-%m-%Y %I:%M:%S %p", time.localtime()))
	self.text_output.insert(tk.END, f'\n{time_str} | {addition}')
	self.text_output.see(tk.END)