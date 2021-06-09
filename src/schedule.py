import requests
import simpleaudio as sa
from src.utils import resource_path
import pandas as pd
from tkinter import messagebox
import json
from src.success import SuccessDialog 

class Schedule():

	def __init__(self, logFn, need_confirmation: bool =True) -> None:

		self.log = logFn
		self.need_confirmation = need_confirmation
	
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

		self.donation_msg = 'If you find the app useful, please consider donating at \n\n rzp.io/l/bookmyslot \n\n60% of all proceeds will be donated to COVID relief.'

		self.confirm_sound = sa.WaveObject.from_wave_file(resource_path('data/confirm.wav'))
		self.success_sound = sa.WaveObject.from_wave_file(resource_path('data/success.wav'))

		self.blocked_centres = []
		# self.captcha = Captcha(self.log)
	
	def book_vaccine(self, token, bfs: list, appointments: pd.DataFrame):

		if len(bfs) == 0 or len(appointments) == 0:
			return

		self.headers['authorization'] = f'Bearer {token}'

		for (dose, under_45), bf_group in bfs.groupby(['dose', 'under_45']):

			names_str = ",".join(list(bf_group['name']))
			
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
				centre_address = appointment['address']
				vaccine = appointment['vaccine']
				price = appointment['price']

				if centre_name in self.blocked_centres:
					self.log(f'Skipping slot in {centre_name}', level='USER')
					continue
				
				vaccine_str = f'Centre name: {centre_name}\nAddress: {centre_address}\nDate: {appointment_date}\nTime: {appointment_time}\nVaccine: {vaccine}\nPrice: {price}\nPeople: {names_str}'

				if self.need_confirmation:
					# Make sound TODO: change sound from captcha to confirm vaccine
					self.confirm_sound.play()

					msgbox = messagebox.askokcancel(
						'Booking confirmation',
						f'{vaccine_str}\n\nClick cancel to skip this centre.',
						icon = 'question'
					)
					if not msgbox:
						self.log(f'I will not try to book a slot in {centre_name} again for this session', level='USER')
						self.blocked_centres.append(centre_name)
						continue

				status = self.try_booking(self.payload, self.headers)

				if (status == 0):
					
					# Remove the beneficiaries from the dataframe
					bfs.drop(bf_group.index, inplace=True)

					self.success_sound.play()

					SuccessDialog(vaccine_str).show()
					
					self.log(f'SCHEDULE.BOOK_VACCINE: {vaccine_str}')
					self.log(f'\n{vaccine_str}', level='USER')
					self.log(f'\n{self.donation_msg}', level='USER')
					break

	
	def try_booking(self, payload, headers):

		response = requests.request("POST", self.url, headers=headers, data=json.dumps(payload))

		status = response.status_code
		if (status == 200):
			data = response.json().get('appointment_id', '')
			msg = f'Appointment ID is {data}'
			ret = 0
		elif status == 400 or status == 409:
			data = ''
			msg = response.json().get('error', '')
			ret = -1
		else:
			data = ''
			msg = response.raw
			ret = -1
		
		self.log(f'SCHEDULE.TRY_BOOKING: {status}={msg}')
		
		return ret

