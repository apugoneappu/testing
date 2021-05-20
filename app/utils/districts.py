import requests
import json

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
