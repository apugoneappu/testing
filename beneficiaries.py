import requests
import logging

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

def get_age(birth_year: int) -> int:

	return 2021-int(birth_year)-1

class Beneficiaries():

	def __init__(self) -> None:

		self.url = "https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"

		self.payload={}
		self.headers = {
			'authority': 'cdn-api.co-vin.in',
			'accept': 'application/json, text/plain, */*',
			'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiI2M2E4MDM2Ni05OWUzLTQwMzktOWU0OS1iN2QwMGQ4ZGUyMWMiLCJ1c2VyX2lkIjoiNjNhODAzNjYtOTllMy00MDM5LTllNDktYjdkMDBkOGRlMjFjIiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo4MDAzMTE1MDYxLCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjIyMjk2Njk0Mjg5NzIwLCJ1YSI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDExXzJfMykgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg5LjAuNDM4OS4xMTQgU2FmYXJpLzUzNy4zNiIsImRhdGVfbW9kaWZpZWQiOiIyMDIxLTA1LTA2VDA3OjQxOjM0LjQ4MloiLCJpYXQiOjE2MjAyODY4OTQsImV4cCI6MTYyMDI4Nzc5NH0.Bi4Xt1McOYyprRpGn4FDfV0mBzCFUpQWkwQOvcZqE8U',
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
			'sec-gpc': '1',
			'origin': 'https://selfregistration.cowin.gov.in',
			'sec-fetch-site': 'cross-site',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'referer': 'https://selfregistration.cowin.gov.in/',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
		}

		self.num_44_or_less = 0
		self.num_45_or_more = 0
		self.bfs = []
	
	def get_beneficiaries(self, token: str):

		self.num_44_or_less = 0
		self.num_45_or_more = 0
		self.bfs = []

		self.headers['authorization'] = f'Bearer {token}'

		response = requests.request("GET", self.url, headers=self.headers, data=self.payload)

		status = response.status_code
		if (status == 200):
			beneficiaries_list = response.json().get('beneficiaries', '')
			msg = f'Found {len(beneficiaries_list)} beneficiaries'
		elif status == 400:
			beneficiaries_list = []
			msg = response.json().get('error', '')
		else:
			beneficiaries_list = []
			msg = response.raw
		
		for bf in beneficiaries_list:

			if (bf['vaccination_status'] =='Vaccinated'):
				continue

			# Don't add vaccinated people
			if (bf['dose1_date'] == ''):
				bf_new_dose_number = 1
			elif (bf['dose2_date'] == ''):
				bf_new_dose_number = 2
			else:
				continue
				
			bf_id = bf['beneficiary_reference_id']
			bf_birth_year = int(bf['birth_year'])
			bf_age = get_age(bf_birth_year)

			if (bf_age <= 44):
				self.num_44_or_less += 1
			else:			
				self.num_45_or_more += 1

			self.bfs.append({
				'id': bf_id,
				'age': bf_age,
				'dose': bf_new_dose_number,
				'under_45': bf_age < 45
			})

		msg = f'Found {len(self.bfs)} valid beneficiaries'
		logger.info(msg)
		
		return self.num_44_or_less, self.num_45_or_more, self.bfs

if __name__ == '__main__':

	from otp import OTP
	otp = OTP()
	txnId = otp.send_otp(7895755566)
	otp_recv = input()
	token = otp.validate_otp(otp_recv, txnId)

	bf = Beneficiaries()
	num_44_or_less, num_45_or_more, bfs = bf.get_beneficiaries(token)

	print(num_44_or_less)
	print(num_45_or_more)
	print(bfs)
