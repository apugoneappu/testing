import requests
import json
import os
import sys
import pandas as pd
import simpleaudio as sa
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)

# Source - https://stackoverflow.com/questions/33595791/blocking-input-dialog-box
class CaptchaDialog(object):
	def __init__(self, centre_name, centre_address, app_date, app_time):
		self.toplevel = tk.Toplevel(window)

		self.toplevel.rowconfigure(0, weight=1)
		self.toplevel.columnconfigure(0, weight=1)

		self.frame_captcha = tk.Frame(master=self.toplevel)
		self.frame_captcha.grid(row=0, column=0, sticky='news')

		self.frame_captcha.rowconfigure([0,1,2], weight=1) 
		self.frame_captcha.columnconfigure(0, weight=2) # frameleft - label, entry
		self.frame_captcha.columnconfigure(1, weight=7) #label

		self.label_booking = tk.Label(master=self.frame_captcha, text=f'Centre name: {centre_name}\nAddress: {centre_address}\nDate: {app_date}\nTime: {app_time}')
		self.label_booking.grid(row=0, column=0, rowspan=1, columnspan=1, sticky='news')

		self.captcha_str = tk.StringVar()
		self.entry_captcha = tk.Entry(master=self.frame_captcha, textvariable=self.captcha_str)
		self.entry_captcha.grid(row=1, column=0, rowspan=1, columnspan=1, sticky='news')

		self.frame_buttons = tk.Frame(master=self.frame_captcha)
		self.frame_buttons.grid(row=2, column=0, rowspan=1, columnspan=1, sticky='news')

		self.button_ok = tk.Button(master=self.frame_buttons, text='OK', command=self.toplevel.destroy)
		self.button_ok.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		self.button_cancel = tk.Button(master=self.frame_buttons, text='Cancel', command=self.toplevel.destroy)
		self.button_cancel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

		# Image right
		loaded_img = Image.open(resource_path('data/captcha.png'))
		self.img = ImageTk.PhotoImage(loaded_img)
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

		with open(resource_path('data/captcha.svg'), "w") as text_file:
   			text_file.write(data.replace('\\', ''))

		drawing = svg2rlg(resource_path('data/captcha.svg'))
		renderPM.drawToFile(drawing, resource_path('data/captcha.png'), fmt="PNG")

		# svg2png(bytestring=data, background_color='white', write_to=resource_path('captcha.png'))

		self.log(f'CAPTCHA.SAVE: Saved captcha image in captcha.png')

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

		self.captcha_sound = sa.WaveObject.from_wave_file(resource_path('data/captcha.wav'))

		self.blocked_centres = []
		self.captcha = Captcha(self.log)
	
	def book_vaccine(self, token, bfs: list, appointments: pd.DataFrame):

		if len(bfs) == 0 or len(appointments) == 0:
			return

		self.headers['authorization'] = f'Bearer {token}'

		for (dose, under_45), bf_group in bfs.groupby(['dose', 'under_45']):
			
			self.payload['beneficiaries'] = list(bf_group.id)
			self.payload['dose'] = int(dose) # needed for converting from np.int64 -> int

			num = len(bf_group)

			dose_appointments = appointments[appointments[f'capacity_dose{dose}'] >= num]

			if (under_45):
				age_grouped_appointments = dose_appointments[appointments.min_age < 45]
			else:
				age_grouped_appointments = dose_appointments[appointments.min_age >= 45]

			age_grouped_appointments = age_grouped_appointments.sort_values(by=['pincode_dist', f'capacity_dose{dose}', 'sort'], ascending=(True, False, True))

			for idx, appointment in age_grouped_appointments.iterrows():

				self.payload["center_id"] = appointment['center_id']
				self.payload["session_id"] = appointment['session_id']
				self.payload["slot"] = appointment['time']

				appointment_date = appointment['date']
				appointment_time = appointment['time']
				centre_name = appointment['name']
				cenre_address = appointment['address']

				if centre_name in self.blocked_centres:
					self.log(f'Skipping slot in {centre_name}', level='USER')
					continue

				# Make sound
				self.captcha_sound.play()

				self.captcha.save(token)
				self.payload['captcha'] = CaptchaDialog(centre_name, cenre_address, appointment_date, appointment_time).show()

				if not self.payload['captcha']:
					self.log(f'I will not try to book a slot in {centre_name} again for this session', level='USER')
					self.blocked_centres.append(centre_name)
					continue

				status = self.try_booking(self.payload, self.headers)

				if (status == 0):
					names_str = " | ".join(list(bf_group['name']))
					
					success_str = f'Vaccine booked on {appointment_date} at {centre_name} for: {names_str}!'

					messagebox.showinfo(
						title='Vaccine booked!', 
						message=success_str
					)
					
					self.log(f'SCHEDULE.BOOK_VACCINE: {success_str}')
					self.log(f'{success_str}', level='USER')
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
