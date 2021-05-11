import tkinter as tk
from tkinter.constants import EXTENDED
import requests
import json
from hashlib import sha256
import os
import sys
from datetime import datetime
import time
import pandas as pd
from cairosvg import svg2png
import simpleaudio as sa
from tkinter import messagebox

TIME_PERIOD_MS = 3500

def resource_path(relative_path):
	 if hasattr(sys, '_MEIPASS'):
		 return os.path.join(sys._MEIPASS, relative_path)
	 return os.path.join(os.path.abspath("."), relative_path)

window = tk.Tk()

# Source - https://stackoverflow.com/questions/33595791/blocking-input-dialog-box
class CaptchaDialog(object):
	def __init__(self):
		self.toplevel = tk.Toplevel(window)

		self.frame_captcha = tk.Frame(master=self.toplevel)
		self.frame_captcha.grid(row=0, column=0, sticky='news')

		self.frame_captcha.rowconfigure([0,1], weight=1) 
		self.frame_captcha.columnconfigure(0, weight=2) # frameleft - label, entry
		self.frame_captcha.columnconfigure(1, weight=7) #label

		self.captcha_str = tk.StringVar()
		self.entry_captcha = tk.Entry(master=self.frame_captcha, textvariable=self.captcha_str)
		self.entry_captcha.grid(row=0, column=0, rowspan=1, columnspan=1)

		self.button_captcha = tk.Button(master=self.frame_captcha, text='OK', command=self.toplevel.destroy)
		self.button_captcha.grid(row=1, column=0, rowspan=1, columnspan=1)

		# Image right
		from PIL import ImageTk, Image
		load = Image.open(resource_path("/tmp/output.png"))
		self.img = ImageTk.PhotoImage(load)
		self.label_image = tk.Label(master=self.frame_captcha, image=self.img)
		self.label_image.image = self.img
		self.label_image.grid(row=0, column=1, sticky='news', rowspan=2, columnspan=1)

	def show(self):
		self.toplevel.grab_set()
		self.toplevel.wait_window()
		value = self.captcha_str.get()
		return value


class Captcha():

	def __init__(self, logFn) -> None:

		self.log = logFn

		self.url = "https://cdn-api.co-vin.in/api/v2/auth/getRecaptcha"

		self.payload = {}
		self.headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			'authorization': 'Bearer <AUTH_TOKEN_HERE>',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'content-type': 'application/json',
			'sec-gpc': '1',
			'origin': 'https://selfregistration.cowin.gov.in',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://selfregistration.cowin.gov.in/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
		}
	
	def save(self, token):

		self.headers['authorization'] = f'Bearer {token}'

		response = requests.request("POST", self.url, headers=self.headers, data=self.payload)

		status = response.status_code
		if status == 200:
			data = response.json().get('captcha', '')
			msg = 'Successfully fetched captcha from server'
		elif status == 400:
			data = ''
			msg = response.json().get('error', '')
		else:
			data = ''
			msg = response.raw

		self.log(f'CAPTCHA.SAVE: {status}={msg}')
		svg2png(bytestring=data, background_color='white', write_to='/tmp/output.png')
		self.log(f'CAPTCHA.SAVE: Saved captcha image in /tmp/output.png')

class Schedule():

	def __init__(self, logFn) -> None:

		self.log = logFn
	
		self.url = "https://cdn-api.co-vin.in/api/v2/appointment/schedule"
		self.payload = {
			"center_id": 619357,
			"captcha": "12AB34",
			"session_id": "80bbd83b-fa1a-4c77-bd8a-e30b8a4e35cd",
			"beneficiaries": [
				"95254777605690"
			],
			"slot": "01:00PM-03:00PM",
			"dose": 1
		}
		self.headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			'authorization': 'Bearer <FILL_TOKEN_HERE>',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'content-type': 'application/json',
			'sec-gpc': '1',
			'origin': 'https://selfregistration.cowin.gov.in',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://selfregistration.cowin.gov.in/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
		}

		self.wave_obj = sa.WaveObject.from_wave_file(resource_path('sound.wav'))

		self.captcha = Captcha(self.log)
	
	def book_vaccine(self, token, bfs: list, appointments: pd.DataFrame):

		if len(bfs) == 0 or len(appointments) == 0:
			return

		self.headers['authorization'] = f'Bearer {token}'

		for (dose, under_45), bf_group in bfs.groupby(['dose', 'under_45']):
			
			self.payload['beneficiaries'] = list(bf_group.id)
			self.payload['dose'] = int(dose) # needed for converting from np.int64 -> int

			if (under_45):
				age_grouped_appointments = appointments[appointments.min_age < 45]
			else:
				age_grouped_appointments = appointments[appointments.min_age >= 45]

			age_grouped_appointments = age_grouped_appointments.sort_values(by=['pincode_dist', 'sort', 'capacity'], ascending=(True, True, False))

			for idx, appointment in age_grouped_appointments.iterrows():

				self.payload["center_id"] = appointment['center_id']
				self.payload["session_id"] = appointment['session_id']
				self.payload["slot"] = appointment['time']

				# Make sound
				play_obj = self.wave_obj.play()

				self.captcha.save(token)
				self.payload['captcha'] = CaptchaDialog().show()

				status = self.try_booking(self.payload, self.headers)

				if (status == 0):
					names_str = " | ".join(list(bf_group['name']))
					appointment_date = appointment['date']
					centre_name = appointment['name']
					success_str = f'Vaccine booked on {appointment_date} at {centre_name} for: {names_str}!'

					messagebox.showinfo(
						title='Vaccine booked!', 
						message=success_str
					)
					
					self.log(f'SCHEDULE.BOOK_VACCINE: {success_str}')
					break

	
	def try_booking(self, payload, headers):

		response = requests.request("POST", self.url, headers=headers, data=json.dumps(payload))

		status = response.status_code
		if (status == 200):
			data = response.json().get('appointment_id', '')
			msg = f'Appointment ID is {data}'
			ret = 0
		elif status == 400:
			data = ''
			msg = response.json().get('error', '')
			ret = -1
		else:
			data = ''
			msg = response.raw
			ret = -1
		
		self.log(f'SCHEDULE.TRY_BOOKING: {status}={msg}')
		
		return ret


class Appointment():

	def __init__(self, logFn, pincode_from, my_pincode, pincode_to) -> None:

		self.log = logFn
		
		self.slots = pd.DataFrame()

		self.pincode_from = int(pincode_from)
		self.my_pincode = int(my_pincode)
		self.pincode_to = int(pincode_to)
		
		self.day = 0
		self.month = 0

		self.url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=%d&date=%02d-%02d-2021"

		self.payload={}
		self.headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			'authorization': f'Bearer <AUTH_TOKEN_HERE>',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'sec-gpc': '1',
			'origin': 'https://selfregistration.cowin.gov.in',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://selfregistration.cowin.gov.in/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
		}

		self.fix_date_month()

	def fix_date_month(self):
		day, month, _ = datetime.today().strftime('%d-%m-%Y').split('-')
		self.day = int(day)
		self.month = int(month)

	def find_slots(self, district_id):

		url = self.url % (district_id, self.day, self.month)

		response = requests.request("GET", url, headers=self.headers, data=self.payload)

		status = response.status_code
		if (status == 200):
			centers = response.json().get('centers', '')
			msg = f'Found {len(centers)} centers'
		elif status == 400:
			centers = []
			msg = response.json().get('error', '')
		else:
			centers = []
			msg = response.raw
		
		self.log(f'APPOINTMENT.FIND_SLOTS: {status}={msg}')

		slots_list = []
		for centre in centers:
			
			name = centre['name']
			centre_id = centre['center_id']
			pincode = centre['pincode']
			sessions = centre['sessions']

			for sess in sessions:

				date = sess['date']
				session_id = sess['session_id']
				min_age = sess['min_age_limit']
				available_capacity = sess['available_capacity']
				slots = sess['slots']

				for time in slots:

					entry = {
						'name': name,
						'center_id': centre_id,
						'pincode': pincode,
						'date': date,
						'session_id': session_id,
						'min_age': min_age,
						'capacity': available_capacity,
						'time': time
					}

					slots_list.append(entry)

		self.slots = pd.DataFrame(slots_list)

		return self.slots
	
	def find_suitable_slots(self, slots: pd.DataFrame, is_44_or_less=1, is_45_or_more=1) -> pd.DataFrame:

		if len(slots) == 0:
			return slots

		slots['pincode_dist'] = abs(slots['pincode'] - self.my_pincode)
		slots['sort'] = slots['date'].str.split('-', expand=True)[0]

		slots = slots[(self.pincode_from <= slots.pincode) & (slots.pincode <= self.pincode_to)]

		slots = slots.sort_values(by=['pincode_dist', 'sort', 'capacity'], ascending=(True, True, False))

		df_44_or_less = slots.copy()
		df_45_or_more = slots.copy()
		
		is_44_or_less = 1e5 if is_44_or_less == 0 else is_44_or_less
		is_45_or_more = 1e5 if is_45_or_more == 0 else is_45_or_more

		df_44_or_less = df_44_or_less[(df_44_or_less.min_age < 45) & (df_44_or_less.capacity >= is_44_or_less)]
		df_45_or_more = df_45_or_more[(df_45_or_more.min_age >= 45) & (df_45_or_more.capacity >= is_45_or_more)]

		final_df = pd.concat([df_44_or_less, df_45_or_more])
		final_df.reset_index(drop=True, inplace=True)

		return final_df



def get_age(birth_year: int) -> int:

	return 2021-int(birth_year)-1

class Beneficiaries():

	def __init__(self, logFn, names: list = []) -> None:

		self.log = logFn

		self.url = "https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"

		self.payload={}
		self.headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			'authorization': 'Bearer <TOKEN_HERE>',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'sec-gpc': '1',
			'origin': 'https://selfregistration.cowin.gov.in',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://selfregistration.cowin.gov.in/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
		}

		self.names = names

	def dose_to_book(self, bf: dict) -> int:

		appointments = bf['appointments']
		vaccination_str = bf['vaccination_status']

		dose_to_book = 0
		for ap in appointments:

			dose = ap['dose']
			dose_to_book = dose if dose > dose_to_book else dose_to_book

			# dose 1 is booked 
			if (dose == 1):
				# if dose 1 not used, then cannot book
				if ('partially' not in vaccination_str.lower()):
					dose_to_book = 3

		dose_to_book += 1

		if (dose_to_book > 2):
			dose_to_book = 0

		return dose_to_book

	def get_beneficiaries(self, token: str):

		self.headers['authorization'] = f'Bearer {token}'

		response = requests.request("GET", self.url, headers=self.headers, data=self.payload)

		status = response.status_code
		if (status == 200):
			bf_list_fetched = response.json().get('beneficiaries', '')
			msg = f'Total {len(bf_list_fetched)} beneficiaries, of which valid are '
		elif status == 400:
			bf_list_fetched = []
			msg = response.json().get('error', '')
		else:
			bf_list_fetched = []
			msg = response.raw

		num_44_or_less = 0
		num_45_or_more = 0
		bf_list_constructed = []
		
		for bf in bf_list_fetched:
			
			name = bf['name']
			if self.names:
				if (name not in self.names):
					continue

			bf_new_dose_number = self.dose_to_book(bf)
			if (bf_new_dose_number == 0):
				continue
				
			bf_id = bf['beneficiary_reference_id']
			bf_birth_year = int(bf['birth_year'])
			bf_age = get_age(bf_birth_year)

			if (bf_age <= 44):
				num_44_or_less += 1
			else:			
				num_45_or_more += 1

			bf_list_constructed.append({
				'name': name,
				'id': bf_id,
				'age': bf_age,
				'dose': bf_new_dose_number,
				'under_45': bf_age < 45
			})
		
		# works even when no beneficiaries
		if (status == 200):
			msg += (" | ").join([b['name'] for b in bf_list_constructed])
			
		self.log(f'BENEFICIARIES.GET_BENEFICIARIES: {status}={msg}')

		return num_44_or_less, num_45_or_more, pd.DataFrame(bf_list_constructed)


class States():
	def __init__(self, logFn) -> None:

		self.log = logFn

		self.url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
		self.payload={}
		self.headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'sec-gpc': '1',
			'origin': 'https://selfregistration.cowin.gov.in',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://selfregistration.cowin.gov.in/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
		}

	def get_states_to_ids(self, data_list: list) -> dict:

		state_to_id_dict = {}

		for d in data_list:
			state_to_id_dict[d['state_name']] = d['state_id']
		
		return state_to_id_dict

	def get_states(self):
		
		response = requests.request("GET", self.url, headers=self.headers, data=self.payload)

		status = response.status_code

		if status == 200:
			data = response.json().get('states', '')
			msg = f'Total {len(data)} states'
		elif status == 400:
			data = ''
			msg = response.json().get('error', '')
		else:
			data = ''
			msg = response.raw

		self.log(f'STATES.GET_STATES: {status}={msg}')
		
		state_to_id_dict = self.get_states_to_ids(data)
		return state_to_id_dict


class Districts():

	def __init__(self, logFn) -> None:

		self.log = logFn

		self.url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/%d"

		self.payload={}
		self.headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'sec-gpc': '1',
			'origin': 'https://selfregistration.cowin.gov.in',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://selfregistration.cowin.gov.in/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
		}

	def get_districts_to_ids(self, data_list: list) -> dict:

		district_to_id_dict = {}

		for d in data_list:
			district_to_id_dict[d['district_name']] = d['district_id']
		
		return district_to_id_dict

	def get_districts(self, state_id: int):

		url = self.url % state_id
		response = requests.request("GET", url, headers=self.headers, data=self.payload)

		status = response.status_code

		if status == 200:
			data = response.json().get('districts', '')
			msg = f'Total {len(data)} districts in chosen state'
		elif status == 400:
			data = ''
			msg = response.json().get('error', '')
		else:
			data = ''
			msg = response.raw

		self.log(f'DISTRICTS.GET_DISTRICTS: {status}={msg}')

		district_to_id_dict = self.get_districts_to_ids(data)
		return district_to_id_dict


class OTP():
	def __init__(self, logFn) -> None:

		self.log = logFn

		self.send_url = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"
		self.send_payload = {
			"secret": "U2FsdGVkX1/XpFGbdwjsUeP/PjBl0AP4QVlJDt8t+6PPaiJFMtlmcUeciyb+XZzQh6Jm6WlZM+nRD/CY6/SpVg==",
			"mobile": 8003115061
		}
		self.send_headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'content-type': 'application/json',
			'sec-gpc': '1',
			'origin': 'https://selfregistration.cowin.gov.in',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://selfregistration.cowin.gov.in/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
		}

		self.validate_url = "https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp"
		self.validate_payload = {
			"otp": "89b4e7cc1899427a932ddeef68a321238098beb02557f6044f6cd81b1cdc4e73",
			"txnId": "c9f55e11-5518-4454-b3a9-db336393c317"
		}
		self.validate_headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'content-type': 'application/json',
			'sec-gpc': '1',
			'origin': 'https://selfregistration.cowin.gov.in',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://selfregistration.cowin.gov.in/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
		}

	def send_otp(self, mobile_number: int) -> str:

		self.send_payload['mobile'] = mobile_number

		response = requests.request("POST", self.send_url, headers=self.send_headers, data=json.dumps(self.send_payload))

		status = response.status_code

		if status == 200:
			data = response.json().get('txnId', '')
			msg = f'txnID is {data}'
		elif status == 400:
			data = ''
			msg = response.json().get('error', '')
		else:
			data = ''
			msg = response.raw

		self.log(f'OTP.SEND_OTP: {status}={msg}')
		return data

	def validate_otp(self, otp: str, txnId: str) -> str:

		self.validate_payload['otp'] = str(sha256(str(otp).encode('utf-8')).hexdigest())
		self.validate_payload['txnId'] = str(txnId)

		response = requests.request("POST", self.validate_url, headers=self.validate_headers, data=json.dumps(self.validate_payload))

		status = response.status_code

		if status == 200:
			data = response.json().get('token', '')
			msg = f'token is {data}'
		elif status == 400:
			data = ''
			msg = response.json().get('error', '')
		else:
			data = ''
			msg = response.raw

		self.log(f'OTP.VALIDATE_OTP: {status}={msg}')
		return data



class GUI():

	def __init__(self) -> None:

		self.logs = ''

		self.window = window
		self.window.title('BookMySlot')

		self.window.geometry("700x500")

		self.window.rowconfigure([0,1,2,3,4,5,6,7], weight=1)
		self.window.rowconfigure(8, weight=2)
		self.window.columnconfigure(0, weight=1)

		######### MOVING OUTPUT TO TOP ##########
		################ Output #################
		self.frame_output = tk.Frame(master=self.window)
		self.frame_output.grid(row=8, column=0, sticky='new')

		self.frame_output.rowconfigure(0, weight=1)
		self.frame_output.rowconfigure(1, weight=10)
		self.frame_output.columnconfigure(0, weight=10)

		self.label_output = tk.Label(master=self.frame_output, text='Output logs', bg='red')
		self.label_output.grid(row=0, column=0)

		# source - https://stackoverflow.com/questions/30669015/autoscroll-of-text-and-scrollbar-in-python-text-box
		self.text_output = tk.Text(self.frame_output)
		self.sb_output = tk.Scrollbar(self.text_output, orient='vertical', command=self.text_output.yview)
		self.text_output.configure(yscrollcommand=self.sb_output.set)
		self.sb_output.grid(sticky='nes')
		self.text_output.grid(sticky='news')
		# self.add_timestamp()

		######### MOVING OUTPUT TO TOP ##########
		self.otp_obj = OTP(self.log)
		self.state_to_id = States(self.log).get_states()
		self.districts = Districts(self.log)

		################ APP NAME #################

		self.frame_app_name = tk.Frame(master=self.window)
		self.frame_app_name.grid(row=0, column=0, sticky='news')

		self.frame_app_name.rowconfigure(0, weight=1)
		self.frame_app_name.columnconfigure(0, weight=1)

		self.label_app_name = tk.Label(master=self.frame_app_name, text='BookMySlot: Covid Vaccine Booking')
		self.label_app_name.grid(row=0, column=0, sticky='news')

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

		self.label_names = tk.Label(master=self.frame_names , text='(Optional) Enter names (comma separated)')
		self.label_names.grid(row=0, column=0, sticky='news')

		self.entry_names = tk.Entry(master=self.frame_names)
		self.entry_names.grid(row=0, column=1, sticky='news')

		################ Locations #################

		self.frame_location = tk.Frame(master=self.window)
		self.frame_location.grid(row=5, column=0, sticky='news')

		self.frame_location.rowconfigure(0, weight=1)
		self.frame_location.columnconfigure(0, weight=1) #state
		self.frame_location.columnconfigure(1, weight=1) #districts

		self.states_list = list(self.state_to_id)
		self.states_str = tk.StringVar(value=self.states_list)
		self.listbox_states = tk.Listbox(self.frame_location, listvariable=self.states_str, height=5)
		self.listbox_states.grid(row=0, column=0, sticky='news')
		self.listbox_states.bind("<<ListboxSelect>>", self.state_selected_callback)

		self.district_list = []
		self.district_str = tk.StringVar(value=self.district_list)
		self.listbox_district = tk.Listbox(self.frame_location, listvariable=self.district_str, height=5, selectmode=EXTENDED)
		self.listbox_district.grid(row=0, column=1, sticky='news')
		self.listbox_district.bind("<<ListboxSelect>>", self.districts_selected_callback)

		################ Submit everything #################

		self.button_submit = tk.Button(master=self.window, text='Submit', command=self.submit_all)
		self.button_submit.grid(row=6, column=0, sticky='news')

		self.button_submit.rowconfigure(0, weight=1)
		self.button_submit.columnconfigure(0, weight=1) 


	def add_timestamp(self):
		self.text_output.insert("end", time.ctime() + "\n")
		self.text_output.see("end")
		self.window.after(1000, self.add_timestamp)	

	
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

		self.tnxId = self.otp_obj.send_otp(mobile)

	def log(self, addition, level='DEBUG'):

		self.text_output.insert(tk.END, f'\n{time.ctime()} | {level} | {addition}')
	
	def state_selected_callback(self, event):

		state_idx = event.widget.curselection()

		if state_idx:
			idx = state_idx[0]
			state_name = self.states_list[idx]
			state_id = self.state_to_id[state_name]

			self.district_to_id = self.districts.get_districts(state_id)
			self.district_list = list(self.district_to_id.keys())
			self.district_str.set(self.district_list)

	def districts_selected_callback(self, event):

		district_idxs = event.widget.curselection()

		self.district_ids = []
		for idx in district_idxs:
			district_name = self.district_list[idx]
			district_id = self.district_to_id[district_name]
			self.district_ids.append(district_id)

		self.log(f'Chosen district ids are {self.district_ids}', level='USER')

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

		self.names = self.entry_names.get()
		if self.names:
			self.names = self.names.split(',')
			self.names = [n.lstrip(' ').rstrip(' ') for n in self.names]
			self.is_names_correct(self.names)

		self.otp = self.entry_otp.get()
		self.token = self.otp_obj.validate_otp(self.otp, self.tnxId)
		if not self.valid_token(self.token):
			return 

		self.pincode_from = self.entry_pincode_from.get()
		self.pincode = self.entry_pincode.get()
		self.pincode_to = self.entry_pincode_to.get()

		self.log('Inputs received', level='USER')

		self.beneficiaries = Beneficiaries(self.log, self.names)
		self.appointment = Appointment(self.log, self.pincode_from, self.pincode, self.pincode_to)
		self.schedule = Schedule(self.log)

		self.log(f'Starting! I will try to book slots once every {TIME_PERIOD_MS/1000} seconds', level='USER')
		self.loop()

	def loop(self):

		num_44_or_less, num_45_or_more, bfs = self.beneficiaries.get_beneficiaries(self.token)

		if len(bfs) == 0:
			self.log('No valid beneficiaries, stopping', level='USER')
			return
		
		slots = []
		for d_code in self.district_ids:
			slots.append(self.appointment.find_slots(d_code))

		slots_comb = pd.concat(slots)
		slots_comb.drop_duplicates(inplace=True, ignore_index=True)

		appointments = self.appointment.find_suitable_slots(slots_comb, num_44_or_less, num_45_or_more)

		self.schedule.book_vaccine(self.token, bfs, appointments)

		# source - https://stackoverflow.com/questions/2400262/how-to-create-a-timer-using-tkinter
		self.window.after(TIME_PERIOD_MS, self.loop)



gui = GUI()
gui.window.mainloop()