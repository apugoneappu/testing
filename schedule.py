import requests
import json
import pandas as pd
import time
import logging
import sys
from captcha import Captcha

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Schedule():

	def __init__(self) -> None:
	
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

		self.captcha = Captcha()
	
	def book_vaccine(self, token, bfs: list, appointments: pd.DataFrame):

		if len(bfs) == 0 or len(appointments) == 0:
			return

		self.headers['authorization'] = f'Bearer {token}'

		self.payload['captcha'] = self.captcha.get(token)

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

				status = self.try_booking(self.payload, self.headers)

				if (status == 0):
					names_str = " | ".join(list(bf_group['name']))
					appointment_date = appointment['date']
					centre_name = appointment['name']
					logging.info(f'Vaccine booked on {appointment_date} at {centre_name} for: {names_str}!')
					break

	
	def try_booking(self, payload, headers):

		response = requests.request("POST", self.url, headers=headers, data=json.dumps(payload))

		status = response.status_code
		if (status == 200):
			data = response.json().get('appointment_id', '')
			msg = f'Appointment id: {data}'
			ret = 0
		elif status == 400:
			data = ''
			msg = response.json().get('error', '')
			ret = -1
		else:
			data = ''
			msg = response.raw
			ret = -1
		
		logger.info(msg)
		
		return ret

if __name__ == '__main__':

	from otp import OTP
	from beneficiaries import Beneficiaries
	from appointment import Appointment
	from captcha import Captcha

	otp = OTP()
	mobile_number = input('Please enter mobile number: \n')
	txnId = otp.send_otp(int(mobile_number))

	otp_recv = input('Please enter OTP: ')
	token = otp.validate_otp(otp_recv, txnId)
	if (token == ''):
		sys.exit('Invalid OTP!')

	district_codes = input('Please enter district range: \n')
	pincodes = input('Please enter pincode range: \n')

	bf = Beneficiaries()

	district_codes = district_codes.split(' ')
	district_codes = list(map(int,district_codes))

	pincodes = pincodes.split(' ')
	pincodes = list(map(int,pincodes))

	ap = Appointment(pincodes[0], pincodes[1], pincodes[2])

	sched = Schedule()

	while (token):
		num_44_or_less, num_45_or_more, bfs = bf.get_beneficiaries(token)

		if (not bfs):
			break
		
		slots = []
		for d_code in district_codes:
			slots.append(ap.find_slots(d_code))

		slots_comb = pd.concat(slots)
		slots_comb.drop_duplicates(inplace=True, ignore_index=True)

		df = ap.find_suitable_slots(slots_comb, num_44_or_less, num_45_or_more)

		if (len(df) > 0):
			sched.book_vaccine(token, bfs, df)

		time.sleep(3.5)




