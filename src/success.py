import tkinter as tk
import webbrowser

class SuccessDialog(object):
	def __init__(self, vaccine_str):
		self.toplevel = tk.Toplevel()

		donation_string = 'If you find the app useful, please consider donating by clicking the button below.\n60% of all proceeds will be donated to COVID relief.'

		self.toplevel.rowconfigure([0,1,2,3], weight=1)
		self.toplevel.columnconfigure(0, weight=1)

		self.label_info = tk.Label(master=self.toplevel, text=vaccine_str)
		self.label_info.grid(row=0, column=0, sticky='news')

		self.label_donate = tk.Label(master=self.toplevel, text=donation_string)
		self.label_donate.grid(row=1, column=0, sticky='news')

		self.button_donate = tk.Button(master=self.toplevel, text='Donate', command=self.donate_callback)
		self.button_donate.grid(row=2, column=0, sticky='news')

		self.button_okay = tk.Button(master=self.toplevel, text='Okay', command=self.okay_callback)
		self.button_okay.grid(row=3, column=0, sticky='news')
	
	def donate_callback(self):
		webbrowser.open('https://pages.razorpay.com/bookmyslot',new=1)

	def okay_callback(self):
		self.toplevel.destroy()

	def show(self):
		self.toplevel.grab_set()
		self.toplevel.wait_window()

if __name__ == '__main__':
	root = tk.Tk()
	vaccine_str = f'Centre name: centre_name\nAddress: centre_address\nDate: appointment_date\nTime: appointment_time\nVaccine: vaccine\nPrice: price\nPeople: names_str'
	dw = SuccessDialog(vaccine_str)
	dw.show()		
	root.mainloop()
