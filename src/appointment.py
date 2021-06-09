import requests
import pandas as pd
from datetime import datetime

class Appointment():

	def __init__(self, logFn, pincode_from, my_pincode, pincode_to, vaccine_names, vaccine_price, token) -> None:

		self.log = logFn

		self.token = token
		
		self.slots = pd.DataFrame()

		self.pincode_from = int(pincode_from)
		self.my_pincode = int(my_pincode)
		self.pincode_to = int(pincode_to)
		self.vaccine_names = [v.lower() for v in vaccine_names]
		self.vaccine_price = vaccine_price
		
		self.day = 0
		self.month = 0

		# self.url = ["https://gb8xvp6u7k.execute-api.ap-south-1.amazonaws.com/cowin-prod/api/v2/appointment/sessions/calendarByDistrict?district_id=%d&date=%02d-%02d-2021", "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=%d&date=%02d-%02d-2021", "https://io8yrvvqbk.execute-api.ap-south-1.amazonaws.com/private-prod/api/v2/appointment/sessions/calendarByDistrict?district_id=%d&date=%02d-%02d-2021"]
		self.url = ["https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=%d&date=%02d-%02d-2021"]

		self.payload={}
		self.headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			# 'authorization': f'Bearer {self.token}',
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
		self.count = 0

	def fix_date_month(self):
		day, month, _ = datetime.today().strftime('%d-%m-%Y').split('-')
		self.day = int(day)
		self.month = int(month)

	def find_slots(self, district_id):
		
		self.count = (self.count + 1) % len(self.url)
		url = self.url[self.count]
		url = url % (district_id, self.day, self.month)

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
			address = centre['address']
			fee_type = centre['fee_type']
			vaccine_fees = centre.get('vaccine_fees', '')

			# If the user has a price pref but the centre does not match it
			if self.vaccine_price and (self.vaccine_price != fee_type):
				continue

			for sess in sessions:

				date = sess['date']
				session_id = sess['session_id']
				min_age = sess['min_age_limit']
				available_capacity = sess['available_capacity']
				slots = sess['slots']
				
				vaccine_name = sess['vaccine']
				# If the user has a vaccine pref
				if self.vaccine_names:
					# But the centre does not have that vaccine
					if vaccine_name.lower() not in self.vaccine_names:
						continue
				
				price = 0
				if vaccine_fees:
					for v_entry in vaccine_fees:

						v_name = v_entry['vaccine']
						v_price = int(v_entry['fee'])

						if v_name == vaccine_name:
							price = v_price

				available_capacity_dose1 = sess['available_capacity_dose1']
				available_capacity_dose2 = sess['available_capacity_dose2']

				for time in slots:

					entry = {
						'name': name,
						'center_id': centre_id,
						'address': address,
						'pincode': pincode,
						'date': date,
						'session_id': session_id,
						'min_age': min_age,
						'capacity': available_capacity,
						'capacity_dose1': available_capacity_dose1,
						'capacity_dose2': available_capacity_dose2,
						'time': time,
						'price': price,
						'vaccine': vaccine_name
					}

					slots_list.append(entry)

		self.slots = pd.DataFrame(slots_list)

		return self.slots
	
	def find_suitable_slots(self, slots: pd.DataFrame, bf_info: pd.DataFrame) -> pd.DataFrame:

		# 'dose': bf_new_dose_number,
		# 'under_45': bf_age < 45

		def fix_num(a):
			b = 1e5 if a == 0 else a
			return b

		num_44_or_less_dose1 = fix_num(len(bf_info[(bf_info.under_45) & (bf_info.dose == 1)]))
		num_44_or_less_dose2 = fix_num(len(bf_info[(bf_info.under_45) & (bf_info.dose == 2)]))

		num_45_or_more_dose1 = fix_num(len(bf_info[(~bf_info.under_45) & (bf_info.dose == 1)]))
		num_45_or_more_dose2 = fix_num(len(bf_info[(~bf_info.under_45) & (bf_info.dose == 2)]))

		if len(slots) == 0:
			return slots

		slots['pincode_dist'] = abs(slots['pincode'] - self.my_pincode)
		slots['sort'] = slots['date'].str.split('-', expand=True)[0]

		slots = slots[(self.pincode_from <= slots.pincode) & (slots.pincode <= self.pincode_to)]

		slots = slots[(slots.capacity_dose1 >= num_44_or_less_dose1) | (slots.capacity_dose1 >= num_45_or_more_dose1) | (slots.capacity_dose2 >= num_44_or_less_dose2) | (slots.capacity_dose2 >= num_45_or_more_dose2)]

		slots = slots.sort_values(by=['pincode_dist', 'capacity_dose1', 'capacity_dose2', 'sort'], ascending=(True, False, False, True))

		df_44_or_less = slots.copy()
		df_45_or_more = slots.copy()
		
		df_44_or_less = df_44_or_less[df_44_or_less.min_age < 45]
		df_44_or_less = df_44_or_less[(df_44_or_less.capacity_dose1 >= num_44_or_less_dose1) | (df_44_or_less.capacity_dose2 >= num_44_or_less_dose2)]

		df_45_or_more = df_45_or_more[df_45_or_more.min_age >= 45]
		df_45_or_more = df_45_or_more[(df_45_or_more.capacity_dose1 >= num_45_or_more_dose1) | (df_45_or_more.capacity_dose2 >= num_45_or_more_dose2)]
		
		final_df = pd.concat([df_44_or_less, df_45_or_more])
		final_df.reset_index(drop=True, inplace=True)

		return final_df
