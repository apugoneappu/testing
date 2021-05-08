import requests
import logging
import pandas as pd

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

def get_age(birth_year: int) -> int:

	return 2021-int(birth_year)-1

class Beneficiaries():

	def __init__(self, names: list = []) -> None:

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
			msg = f'Found {len(bf_list_fetched)} beneficiaries'
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
		valid_names = (" | ").join([b['name'] for b in bf_list_constructed])
		msg = f'Valid beneficiaries: {valid_names}'
		logger.info(msg)
		
		return num_44_or_less, num_45_or_more, pd.DataFrame(bf_list_constructed)

if __name__ == '__main__':

	from otp import OTP
	otp = OTP()
	txnId = otp.send_otp(8003115061)
	otp_recv = input()
	token = otp.validate_otp(otp_recv, txnId)

	bf = Beneficiaries(names=['Anju Devi', 'Pushpa Devi'])
	num_44_or_less, num_45_or_more, bfs = bf.get_beneficiaries(token)

	print(num_44_or_less)
	print(num_45_or_more)
	print(bfs)
