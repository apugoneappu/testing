import requests
from datetime import datetime
import pandas as pd
import logging

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

class Appointment():

	def __init__(self, pincode_from, my_pincode, pincode_to) -> None:

		self.slots = pd.DataFrame()

		self.pincode_from = pincode_from
		self.my_pincode = my_pincode
		self.pincode_to = pincode_to
		
		self.day = 0
		self.month = 0

		self.url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=%d&date=%02d-%02d-2021"

		self.payload={}
		self.headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			'authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJkMDk5Y2I4OS05YWUxLTQ3YTEtOTEwMS1mNmFjNDRiMzViNzAiLCJ1c2VyX2lkIjoiZDA5OWNiODktOWFlMS00N2ExLTkxMDEtZjZhYzQ0YjM1YjcwIiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo4MDAzMTE1MDYxLCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjk1MjU0Nzc3NjA1NjkwLCJ1YSI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDExXzJfMykgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg5LjAuNDM4OS4xMTQgU2FmYXJpLzUzNy4zNiIsImRhdGVfbW9kaWZpZWQiOiIyMDIxLTA1LTA2VDA2OjUwOjMwLjM2NVoiLCJpYXQiOjE2MjAyODM4MzAsImV4cCI6MTYyMDI4NDczMH0.pCO8s0JVQR5w4-1iGaDzwDnFmVBUK7ckN-LDs24M8xw',
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
		
		logger.info(msg)

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


if __name__ == '__main__':

	from otp import OTP
	from beneficiaries import Beneficiaries

	# otp = OTP()
	# txnId = otp.send_otp(8003115061)
	# otp_recv = input('Please enter OTP: ')
	# token = otp.validate_otp(otp_recv, txnId)

	# bf = Beneficiaries()
	# num_44_or_less, num_45_or_more, bfs = bf.get_beneficiaries(token)

	ap = Appointment(302000, 302006, 304000)

	district_codes = [505, 506]
	
	slots = []
	for d_code in district_codes:
		slots.append(ap.find_slots(d_code))

	slots_comb = pd.concat(slots)
	slots_comb.drop_duplicates(inplace=True, ignore_index=True)

	df = ap.find_suitable_slots(slots_comb, num_44_or_less=3, num_45_or_more=2)




