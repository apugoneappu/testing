import requests
import json
import pandas as pd
from utils.utils import get_age

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

		bf_info = []
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

			bf_info.append(
				{
					'dose': bf_new_dose_number,
					'under_45': bf_age < 45
				}
			)

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
		self.log(f'{msg}', level='USER')

		return pd.DataFrame(bf_info), pd.DataFrame(bf_list_constructed)
