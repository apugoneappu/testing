__version__ = "1.0.1"

import kivy
kivy.require("1.11.1") # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.animation import Animation

# import pandas as pd
from utils.otp import OTP, valid_token
from utils.states import States
from utils.districts import Districts
from utils.beneficiaries import Beneficiaries
from utils.appointment import Appointment
from utils.utils import log, is_number_correct, is_names_correct

TIME_PERIOD_MS = 3500

class MyLayout(Widget):
	
	def __init__(self, **kwargs):
		self.mobile_number_input = ObjectProperty(None)
		self.otp_input = ObjectProperty(None)
		self.pincode_input = ObjectProperty(None)
		self.names_input = ObjectProperty(None)

		self.otp_fn = OTP(log)
		self.state_fn = States(log)
		self.district_fn = Districts(log)
		# self.schedule_fn = Schedule(log)
		# self.timer_fn = CountDownTimer()

		self.build_state_list()

		super().__init__(**kwargs)

	def get_otp_callback(self):
		mobile_number = self.mobile_number_input.text
		if not is_number_correct(mobile_number, 10, 'mobile number'):
			return		
		mobile_number = int(mobile_number)

		self.txnId = self.otp_fn.send_otp(mobile_number)

	def build_state_list(self):
		self.states_dict = self.state_fn.get_states()
		self.states_list = list(self.states_dict.keys())

	def state_selected_callback(self, state_name):
		state_id = self.states_dict[state_name]
		log(f'Chosen state is {state_name}')

		self.districts_dict = self.district_fn.get_districts(state_id)
		self.ids.district_spinner.values = list(self.districts_dict.keys())

	def districts_selected_callback(self, district_name):
		self.district_ids = []
		self.district_ids.append(self.districts_dict[district_name])
		self.district_name = district_name
		log(f'Chosen districts are {self.district_name}')

	def submit_all(self):

		entry_mobile = self.mobile_number_input.text
		entry_otp = self.otp_input.text
		entry_pincode = self.pincode_input.text
		entry_names = self.names_input.text
		entry_pincode_from = '000000'
		entry_pincode_to = '999999'

		if not is_number_correct(entry_mobile, 10, 'Mobile Number'):
			return

		if not is_number_correct(entry_otp, 6, 'OTP Code'):
			return

		if not is_number_correct(entry_pincode_from, 6, 'Pincode From'):
			return

		if not is_number_correct(entry_pincode, 6, 'Pincode'):
			return

		if not is_number_correct(entry_pincode_to, 6, 'Pincode To'):
			return

		if entry_names:
			entry_names = entry_names.split(',')
			entry_names = [n.lstrip(' ').rstrip(' ') for n in entry_names]
			is_names_correct(entry_names)

		self.token = self.otp_fn.validate_otp(entry_otp, self.txnId)
		if not valid_token(self.token):
			return 

		# Start countdown
		# self.countdown_timer.start()

		log(f'You have chosen the districts {self.district_name}', level='USER')

		if entry_names:
			names_str = ", ".join(entry_names)
			log(f"I will only try to book slots for {names_str}. Please ensure that these names have the same spelling as registered on the CoWIN website.", level='USER')

		log(f'I will book slots nearest to the pincode {entry_pincode}, and only between pincodes {entry_pincode_from} and {entry_pincode_to} so it is not too far away from your house.', level='USER')

		self.beneficiaries_fn = Beneficiaries(log, entry_names)
		self.appointment_fn = Appointment(log, entry_pincode_from, entry_pincode, entry_pincode_to)

		# Disable all inputs except otp
		self.is_stop = False
		# self.disable_all_inputs()

		log(f'Starting! I will look for new slots every {TIME_PERIOD_MS/1000} seconds', level='USER')
		# self.loop()

	# def loop(self):

	# 	if self.is_stop:
	# 		return

	# 	bf_info, bfs = self.beneficiaries_fn.get_beneficiaries(self.token)

	# 	if len(bfs) == 0:
	# 		self.stop()
	# 		return
		
	# 	slots = []
	# 	for d_code in self.district_ids:
	# 		slots.append(self.appointment_fn.find_slots(d_code))

	# 	slots_comb = pd.concat(slots)
	# 	slots_comb.drop_duplicates(inplace=True, ignore_index=True)

	# 	appointments = self.appointment_fn.find_suitable_slots(slots_comb, bf_info)

		# self.schedule.book_vaccine(self.token, bfs, appointments)

		# source - https://stackoverflow.com/questions/2400262/how-to-create-a-timer-using-tkinter
		# self.window.after(TIME_PERIOD_MS, self.loop)

	# def disable_all_inputs(self):

	# 	self.entry_mobile.configure(state=tk.DISABLED)
	# 	self.entry_pincode.configure(state=tk.DISABLED)
	# 	self.entry_pincode_from.configure(state=tk.DISABLED)
	# 	self.entry_pincode_to.configure(state=tk.DISABLED)
	# 	self.entry_names.configure(state=tk.DISABLED)
		
	# 	self.listbox_states.configure(state=tk.DISABLED, highlightbackground='blue')
	# 	self.listbox_district.configure(state=tk.DISABLED, highlightbackground='blue')

	# 	self.toggle_submit_stop_buttons()

	def stop(self):

		# self.countdown_timer.stop_and_reset()
		# self.logout_sound.play()
		# messagebox.showwarning('Session logged out', 'Session logged out! Please relogin using a new OTP')
		print('Session logged out', 'Session logged out! Please relogin using a new OTP')
		
		self.is_stop = True
		self.toggle_submit_stop_buttons()
		log('Stopping search! Please login again with a new OTP.', level='USER')

	def toggle_submit_stop_buttons(self):

		assert self.button_submit['state'] != self.button_stop['state'], \
			f"Submit button: {self.button_submit['state']} and Stop button: {self.button_stop['state']}"

		# def invert_state(widget):

		# 	if widget['state'] == tk.NORMAL:
		# 		widget.configure(state=tk.DISABLED)
		# 	else:
		# 		widget.configure(state=tk.NORMAL)
		
		# invert_state(self.button_submit)
		# invert_state(self.button_stop)

class MyApp(App):
	def build(self):
		return MyLayout()

if __name__ == "__main__":
	MyApp().run()