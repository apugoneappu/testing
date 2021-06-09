import requests
import json
from hashlib import sha256

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
		elif status == 401:
			data = ''
			msg = 'Unauthorized access! Please check the OTP or generate a new OTP.'
		else:
			data = ''
			msg = response.raw

		self.log(f'OTP.VALIDATE_OTP: {status}={msg}')
		return data
