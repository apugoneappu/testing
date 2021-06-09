import tkinter as tk

import time
import pandas as pd
import simpleaudio as sa
from tkinter import messagebox
from src.update import UpdateChecker
from src.schedule import Schedule
from src.utils import resource_path
from src.appointment import Appointment
from src.places import States, Districts
from src.otp import OTP
from src.timer import CountDownTimer
from src.beneficiaries import Beneficiaries


###############################################################
TIME_PERIOD_MS = 3500
CURRENT_VERSION = '5.0.0'
###############################################################

class GUI():

	def __init__(self) -> None:

		self.window = tk.Tk()
		self.window.title(f'BookMySlot (version: {CURRENT_VERSION})')

		self.window.geometry("800x700")

		self.window.rowconfigure(6, weight=1)
		self.window.rowconfigure(8, weight=10)
		self.window.columnconfigure(0, weight=1)

		self.uc = UpdateChecker()

		######### MOVING OUTPUT TO TOP ##########
		################ Output #################
		self.frame_output = tk.Frame(master=self.window)
		self.frame_output.grid(row=8, column=0, sticky='news')

		self.frame_output.rowconfigure(0, weight=0, minsize=10)
		self.frame_output.rowconfigure(1, weight=1, minsize=50)
		self.frame_output.columnconfigure(0, weight=10)

		self.label_output = tk.Label(master=self.frame_output, text='Output logs:')
		self.label_output.grid(row=0, column=0, sticky='nw')

		# source - https://stackoverflow.com/questions/30669015/autoscroll-of-text-and-scrollbar-in-python-text-box
		self.frame_right = tk.Frame(master=self.frame_output)
		self.frame_right.grid(row=1, column=0, sticky='news')

		self.text_output = tk.Text(self.frame_right)
		self.sb_output = tk.Scrollbar(master=self.frame_right, orient='vertical', command=self.text_output.yview)
		self.text_output.configure(yscrollcommand=self.sb_output.set)
		self.sb_output.pack(fill=tk.Y, side=tk.RIGHT)
		self.text_output.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

		######### MOVING OUTPUT TO TOP ##########
		self.otp_obj = OTP(self.log)
		self.state_to_id = States(self.log).get_states()
		self.districts = Districts(self.log)

		################ APP NAME AND COUNTDOWN TIMER #################

		self.frame_app_name = tk.Frame(master=self.window)
		self.frame_app_name.grid(row=0, column=0, sticky='news')

		self.frame_app_name.rowconfigure(0, weight=1)
		self.frame_app_name.columnconfigure(0, weight=1)
		self.frame_app_name.columnconfigure(1, weight=0)

		self.label_app_name = tk.Label(master=self.frame_app_name, text='BookMySlot: Covid Vaccine Booking')
		self.label_app_name.grid(row=0, column=0, sticky='news')

		self.str_timer = tk.StringVar()
		self.label_timer = tk.Label(master=self.frame_app_name, textvariable=self.str_timer)
		self.countdown_timer = CountDownTimer(self.label_timer, self.str_timer)
		self.label_timer.grid(row=0, column=1, sticky='nsw', padx=20)


		################ MOBILE #################

		self.frame_mobile = tk.Frame(master=self.window)
		self.frame_mobile.grid(row=1, column=0, sticky='news')

		self.frame_mobile.rowconfigure(0, weight=1)
		self.frame_mobile.columnconfigure(0, weight=2) #label
		self.frame_mobile.columnconfigure(1, weight=5) #entry
		self.frame_mobile.columnconfigure(2, weight=2) #button

		self.label_mobile = tk.Label(master=self.frame_mobile , text='Mobile number')
		self.label_mobile.grid(row=0, column=0, sticky='news')

		self.entry_mobile = tk.Entry(master=self.frame_mobile)
		self.entry_mobile.grid(row=0, column=1, sticky='news')

		self.button_mobile = tk.Button(master=self.frame_mobile, text='Get OTP', command=self.get_otp_callback)
		self.button_mobile.grid(row=0, column=2, sticky='news')

		################ OTP #################

		self.frame_otp = tk.Frame(master=self.window)
		self.frame_otp.grid(row=2, column=0, sticky='news')

		self.frame_otp.rowconfigure(0, weight=1)
		self.frame_otp.columnconfigure(0, weight=2) #label
		self.frame_otp.columnconfigure(1, weight=7) #entry

		self.label_otp = tk.Label(master=self.frame_otp , text='OTP number')
		self.label_otp.grid(row=0, column=0, sticky='news')

		self.entry_otp = tk.Entry(master=self.frame_otp)
		self.entry_otp.grid(row=0, column=1, sticky='news')

		################ Pincode #################

		self.frame_pincode = tk.Frame(master=self.window)
		self.frame_pincode.grid(row=3, column=0, sticky='news')

		self.frame_pincode.rowconfigure(0, weight=1)
		self.frame_pincode.columnconfigure([0,2,4], weight=2) #labels
		self.frame_pincode.columnconfigure([1,3,5], weight=7) #entries

		self.label_pincode_from = tk.Label(master=self.frame_pincode , text='Pincode from')
		self.label_pincode_from.grid(row=0, column=0, sticky='news')

		pincode_from_init = tk.StringVar(value='000000')
		self.entry_pincode_from = tk.Entry(master=self.frame_pincode, textvariable=pincode_from_init)
		self.entry_pincode_from.grid(row=0, column=1, sticky='news')

		self.label_pincode = tk.Label(master=self.frame_pincode, text='Pincode')
		self.label_pincode.grid(row=0, column=2, sticky='news')

		self.entry_pincode = tk.Entry(master=self.frame_pincode)
		self.entry_pincode.grid(row=0, column=3, sticky='news')

		self.label_pincode_to = tk.Label(master=self.frame_pincode , text='Pincode to')
		self.label_pincode_to.grid(row=0, column=4, sticky='news')

		pincode_to_init = tk.StringVar(value='999999')
		self.entry_pincode_to = tk.Entry(master=self.frame_pincode, textvariable=pincode_to_init)
		self.entry_pincode_to.grid(row=0, column=5, sticky='news')

		################ Names #################

		self.frame_names = tk.Frame(master=self.window)
		self.frame_names.grid(row=4, column=0, sticky='news')

		self.frame_names.rowconfigure(0, weight=1)
		self.frame_names.columnconfigure(0, weight=2) #label
		self.frame_names.columnconfigure(1, weight=7) #entry

		self.frame_bf_auto = tk.Frame(self.frame_names)
		self.frame_bf_auto.rowconfigure([0,1], weight=1)
		self.frame_bf_auto.columnconfigure(0, weight=1)

		self.frame_bf_auto.grid(row=0, column=0, sticky='news')


		self.button_names = tk.Button(self.frame_bf_auto, text='Get beneficiaries', command=self.get_beneficiaries_callback)
		self.button_names.grid(row=0, column=0, sticky='ew')

		self.need_confirmation = tk.BooleanVar(value=True)
		self.checkbox_auto = tk.Checkbutton(self.frame_bf_auto, text='Confirm slot details before booking', offvalue=False, onvalue=True, variable=self.need_confirmation, command=self.book_without_confirmation)
		self.checkbox_auto.grid(row=1, column=0, sticky='ew')

		self.frame_listbox_names = tk.Frame(self.frame_names)
		self.frame_listbox_names.grid(row=0, column=1, sticky='news')

		names_list = ["Please click the 'Get beneficiaries button'"]
		self.names_str = tk.StringVar(value=names_list)
		self.listbox_names = tk.Listbox(self.frame_listbox_names, listvariable=self.names_str, height=5, selectmode=tk.MULTIPLE, exportselection=False)
		self.listbox_names.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.listbox_names.bind("<<ListboxSelect>>", self.names_selected_callback)
		self.sb_names = tk.Scrollbar(master=self.frame_listbox_names, orient='vertical', command=self.
		listbox_names.yview)
		self.listbox_names.configure(yscrollcommand=self.sb_names.set)
		self.sb_names.pack(side=tk.RIGHT, fill=tk.Y)


		################ Options ###################

		self.frame_options = tk.Frame(master=self.window)
		self.frame_options.grid(row=5, column=0, sticky='news')

		self.frame_options.rowconfigure(0, weight=1)
		self.frame_options.columnconfigure([0,1], weight=1) #both

		self.frame_vaccine = tk.Frame(self.frame_options)
		self.frame_vaccine.grid(row=0, column=0, sticky='news')

		self.label_vaccine = tk.Label(self.frame_vaccine, text=' (Optional) Vaccine name(s) (comma separated) ')
		self.label_vaccine.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		self.entry_vaccine = tk.Entry(self.frame_vaccine)
		self.entry_vaccine.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

		# vaccine_options = ['Any', 'Covishield', 'Covaxin', 'Sputnik V']
		# self.vaccine_name = tk.StringVar()
		# self.vaccine_name.set('Any')
		# self.menu_vaccine = tk.OptionMenu(self.frame_vaccine, self.vaccine_name, *vaccine_options)
		# self.menu_vaccine.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		self.frame_price = tk.Frame(self.frame_options)
		self.frame_price.grid(row=0, column=1, sticky='news')

		self.label_price = tk.Label(self.frame_price, text='Vaccine cost')
		self.label_price.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		price_options = ['Any', 'Free', 'Paid']
		self.string_price = tk.StringVar()
		self.string_price.set('Any')
		self.menu_price = tk.OptionMenu(self.frame_price, self.string_price, *price_options)
		self.menu_price.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


		################ Locations #################

		self.frame_location = tk.Frame(master=self.window)
		self.frame_location.grid(row=6, column=0, sticky='news')

		self.frame_location.rowconfigure(0, weight=1)
		self.frame_location.columnconfigure(0, weight=1) #state
		self.frame_location.columnconfigure(1, weight=1) #districts

		self.frame_states = tk.Frame(master=self.frame_location)
		self.frame_states.grid(row=0, column=0, sticky='news')

		self.label_states = tk.Label(self.frame_states, text='Choose state')
		self.label_states.pack(side=tk.TOP, anchor=tk.NW)

		self.states_list = list(self.state_to_id.keys())
		self.states_str = tk.StringVar(value=self.states_list)
		self.listbox_states = tk.Listbox(self.frame_states, listvariable=self.states_str, height=7, exportselection=False)
		self.listbox_states.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.listbox_states.bind("<<ListboxSelect>>", self.state_selected_callback)
		self.sb_states = tk.Scrollbar(master=self.frame_states, orient='vertical', command=self.
		listbox_states.yview)
		self.listbox_states.configure(yscrollcommand=self.sb_states.set)
		self.sb_states.pack(side=tk.RIGHT, fill=tk.Y)


		self.frame_district = tk.Frame(master=self.frame_location)
		self.frame_district.grid(row=0, column=1, sticky='news')

		self.label_district = tk.Label(self.frame_district, text='Choose district(s) (click to select, click again to deselect)')
		self.label_district.pack(side=tk.TOP, anchor=tk.NW)
		
		self.district_list = []
		self.district_str = tk.StringVar(value=self.district_list)
		self.listbox_district = tk.Listbox(self.frame_district, listvariable=self.district_str, height=7, selectmode=tk.MULTIPLE, exportselection=False)
		self.listbox_district.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.listbox_district.bind("<<ListboxSelect>>", self.districts_selected_callback)
		self.sb_district = tk.Scrollbar(master=self.frame_district, orient='vertical', command=self.
		listbox_district.yview)
		self.listbox_district.configure(yscrollcommand=self.sb_district.set)
		self.sb_district.pack(side=tk.RIGHT, fill=tk.Y)


		################ Submit everything #################

		self.frame_button_row = tk.Frame(self.window)
		self.frame_button_row.grid(row=7, column=0, sticky='news')

		self.button_submit = tk.Button(master=self.frame_button_row, text='Start', command=self.submit_all)
		self.button_submit.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

		self.button_stop = tk.Button(master=self.frame_button_row, text='Stop', command=self.stop)
		self.button_stop.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.button_stop.configure(state=tk.DISABLED)

		####### INIT ########
		self.selected_bfs = []
		self.is_stop = False
		self.logout_sound = sa.WaveObject.from_wave_file(resource_path('data/login.wav'))
		self.tnxId = ''
		self.log(
		'\n----------------------------------------------------------------------------------------\n'
		'\nIMPORTANT INSTRUCTIONS: \n'
		'\n1. To book slots for only 18+ category, choose only those beneficiaries from the names.\n'
		'\n2. The vaccine names field is used to selectively look for slots of only some types of vaccine. Leaving it empty means you want to book for all available vaccine types. Please use the options: "Covishield", "Covaxin", "Sputnik V"  \nExample - Covishield, Covaxin.\n'
		'\n3. "Pincode from" and "Pincode to" fields are used to restrict the range of pincodes in which to book slots. This is done so that the vaccination centre is not too far away from you. The "Pincode" field is used to book slots as close to you as possible. \nExample - pincode from=302000, pincode=302005, pincode to = 302050 would try to book slots between 302000 and 302050, as close to 302005 as possible.\n\n'
		'Please report issues at contact@bookmyslot.life'
		'\n----------------------------------------------------------------------------------------\n', level='USER')

		self.close_if_not_latest()


	def close_if_not_latest(self):

		latest = self.uc.get_latest_version()

		if latest:
			if latest != CURRENT_VERSION:
				messagebox.showerror(
					'Old Version',
					f'Please download the latest version {latest} from www.bookmyslot.life\nYour current version is {CURRENT_VERSION}'
				)
				self.window.destroy()

	
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

	def is_names_correct(self, names_list: list):

		if names_list:
			print_str = "\n".join(names_list)
			messagebox.showinfo(title='Entered names', 
				message=f'The entered names should have exact names registered on Cowin:\n {print_str}'
			)
	
	def valid_token(self, token):

		if not token:
			self.entry_otp.configure(background='salmon')
			messagebox.showerror(title='The entered OTP is incorrect', 
				message=f'The entered OTP is incorrect. Please get a new OTP code by clicking Get OTP.'
			)
			return False
		else:
			self.entry_otp.configure(background='pale green')
			return True
	
	def get_otp_callback(self):

		mobile = self.entry_mobile.get()
		if not self.is_number_correct(self.entry_mobile, 10, 'mobile number'):
			return
		mobile = int(mobile)

		tnxId = self.otp_obj.send_otp(mobile)

		if (tnxId != self.tnxId):
			self.log('New OTP generated', level='USER')
		else:
			self.log('Please use the last OTP', level='USER')

		self.tnxId = tnxId

	def log(self, addition, level='DEBUG'):

		if (level == 'DEBUG'):
			return

		time_str = str(time.strftime("%d-%m-%Y %I:%M:%S %p", time.localtime()))
		self.text_output.insert(tk.END, f'{time_str} | {addition} \n')
		self.text_output.see(tk.END)
	
	def state_selected_callback(self, event):

		state_idx = event.widget.curselection()

		if state_idx:
			idx = state_idx[0]
			state_name = self.states_list[idx]
			state_id = self.state_to_id[state_name]

			self.log(f'Chosen state is {state_name}')

			self.district_to_id = self.districts.get_districts(state_id)
			self.district_list = list(self.district_to_id.keys())
			self.district_str.set(self.district_list)


	def districts_selected_callback(self, event):

		district_idxs = event.widget.curselection()

		self.district_ids = []
		district_names = []
		for idx in district_idxs:
			district_name = self.district_list[idx]
			district_id = self.district_to_id[district_name]
			self.district_ids.append(district_id)
			district_names.append(district_name)

		self.district_name_joined = ", ".join(district_names)
		self.log(f'Chosen districts are {self.district_name_joined}')
	
	def is_logged_in(self):

		self.otp = self.entry_otp.get()
		self.token = self.otp_obj.validate_otp(self.otp, self.tnxId)

		return self.valid_token(self.token)
	
	def get_beneficiaries_callback(self):

		if not self.is_logged_in():
			return
		
		self.beneficiaries = Beneficiaries(self.log)
		self.bfs = self.beneficiaries.get_beneficiaries(self.token)

		self.names_str.set(list(self.bfs['name']))

	def names_selected_callback(self, event):

		name_idxs = event.widget.curselection()

		if name_idxs:
			self.selected_bfs = self.bfs.iloc[list(name_idxs)]

	def stop(self):

		self.countdown_timer.stop_and_reset()
		self.logout_sound.play()
		messagebox.showwarning('Session logged out', 'Session logged out! Please relogin using a new OTP')
		
		self.is_stop = True
		self.toggle_inputs()
		self.log('Stopping search! Please login again with a new OTP.', level='USER')

	def invert_state(self, widget):

		if widget['state'] == tk.NORMAL:
			widget.configure(state=tk.DISABLED)
		else:
			widget.configure(state=tk.NORMAL)
	
	def toggle_inputs(self):
		
		self.invert_state(self.button_submit)
		self.invert_state(self.button_stop)
		self.invert_state(self.entry_mobile)
		self.invert_state(self.entry_pincode)
		self.invert_state(self.entry_pincode_from)
		self.invert_state(self.entry_pincode_to)
		self.invert_state(self.listbox_states)
		self.invert_state(self.listbox_district)
		self.invert_state(self.entry_vaccine)
		self.invert_state(self.menu_price)

	def book_without_confirmation(self):

		if not self.need_confirmation.get():
			msg = messagebox.askokcancel(
				title='Booking without confirmation',
				message='You have chosen to book a slot without confirmation. This may lead to slot booking in an unwanted centre.\n\nPress OK if you would like to proceed.\nPress cancel to change your preference.'
			)

			if not msg:
				self.checkbox_auto.select()

	def submit_all(self):

		if not self.is_number_correct(self.entry_mobile, 10, 'Mobile Number'):
			return

		if not self.is_number_correct(self.entry_otp, 6, 'OTP Code'):
			return

		if not self.is_number_correct(self.entry_pincode_from, 6, 'Pincode From'):
			return

		if not self.is_number_correct(self.entry_pincode, 6, 'Pincode'):
			return

		if not self.is_number_correct(self.entry_pincode_to, 6, 'Pincode To'):
			return

		if len(self.selected_bfs) == 0:
			messagebox.showerror('Select names', 'Please choose some names')
			return

		# Start countdown
		self.countdown_timer.start()

		self.pincode_from = self.entry_pincode_from.get()
		self.pincode = self.entry_pincode.get()
		self.pincode_to = self.entry_pincode_to.get()

		self.vaccine_names = self.entry_vaccine.get()
		if self.vaccine_names:
			self.vaccine_names = self.vaccine_names.split(',')
			self.vaccine_names = [n.lstrip(' ').rstrip(' ') for n in self.vaccine_names]
			vacc_name_str = "\n".join(self.vaccine_names)
			messagebox.showinfo(
				title='Vaccine name', 
				message=f'Vaccine names should exactly match as given on CoWIN:\n{vacc_name_str}'
			)

		self.vaccine_price = self.string_price.get()
		if self.vaccine_price == 'Any':
			self.vaccine_price = ''

		self.log(f'You have chosen the districts {self.district_name_joined}', level='USER')

		self.log(f'I will book slots nearest to the pincode {self.pincode}, and only between pincodes {self.pincode_from} and {self.pincode_to} so it is not too far away from your house.', level='USER')

		names_str = ", ".join(list(self.selected_bfs['name']))
		self.log(f"I will only try to book slots for {names_str}.", level='USER')
		self.beneficiaries.set_names(list(self.selected_bfs['name']))

		self.appointment = Appointment(self.log, self.pincode_from, self.pincode, self.pincode_to, self.vaccine_names, self.vaccine_price, self.token)
		self.schedule = Schedule(self.log, self.need_confirmation.get())

		# Disable all inputs except otp
		self.is_stop = False
		self.toggle_inputs()

		self.log(f'Starting! I will look for new slots every {TIME_PERIOD_MS/1000} seconds', level='USER')
		self.loop()

	def loop(self):

		if self.is_stop:
			return

		if len(self.selected_bfs) == 0 or len(self.beneficiaries.get_beneficiaries(self.token)) == 0:
			self.log('No more valid beneficiaries found. Stopping search.', level='USER')
			self.stop()
			return

		slots = []
		for d_code in self.district_ids:
			slots.append(self.appointment.find_slots(d_code))

		slots_comb = pd.concat(slots)
		slots_comb.drop_duplicates(inplace=True, ignore_index=True)

		appointments = self.appointment.find_suitable_slots(slots_comb, self.selected_bfs)

		self.log(f'Found {len(slots_comb)} slots of which {len(appointments)} are valid.', level='USER')

		self.schedule.book_vaccine(self.token, self.selected_bfs, appointments)

		# source - https://stackoverflow.com/questions/2400262/how-to-create-a-timer-using-tkinter
		self.window.after(TIME_PERIOD_MS, self.loop)


gui = GUI()
gui.window.mainloop()
