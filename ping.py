import requests
import time
from datetime import datetime
import json

#################### PARAMS #####################
min_age_below=30
min_available_capacity=2
#################################################

def generate_otp(mobile_number_str: str):

	url = "https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP"

	payload = json.dumps({
		"mobile": mobile_number_str
	})
	headers = {
		'accept': 'application/json',
		'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	if (response.status_code == 200):
		print(f'OTP generated for {mobile_number_str}')
	else:
		print(f'OTP error {response.status_code} for {mobile_number_str}')

	return

def get_district_name(district_id):

	if (district_id == 505):
		return "Jaipur 1"

	elif (district_id == 506):
		return "Jaipur 2"
	
	else:
		raise NotImplementedError


def send_notification(string):

	print(string)

	NOTIF_URL = "https://maker.ifttt.com/trigger/vaccine_available/with/key/bx-gv6c4m0BUSKu_l0a0gu"

	notif_resp = requests.get(NOTIF_URL, params={"value1": string})

def check_7_days_from(day, month, min_age_below, min_available_capacity, district_id) -> int:

	url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=%d&date=%02d-%02d-2021" % (district_id, day, month)

	payload={}
	headers = {
		'authority': 'cdn-api.co-vin.in',
		'accept': 'application/json, text/plain, */*',
		'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJkMDk5Y2I4OS05YWUxLTQ3YTEtOTEwMS1mNmFjNDRiMzViNzAiLCJ1c2VyX2lkIjoiZDA5OWNiODktOWFlMS00N2ExLTkxMDEtZjZhYzQ0YjM1YjcwIiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo4MDAzMTE1MDYxLCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjk1MjU0Nzc3NjA1NjkwLCJ1YSI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDExXzJfMykgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg5LjAuNDM4OS4xMTQgU2FmYXJpLzUzNy4zNiIsImRhdGVfbW9kaWZpZWQiOiIyMDIxLTA1LTA1VDE2OjA1OjMwLjkyNloiLCJpYXQiOjE2MjAyMzA3MzAsImV4cCI6MTYyMDIzMTYzMH0.phX-C_n5YBdwwfTOp2YzX0ziG7tK1cdkbB03z6Wk7m8',
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
		'sec-gpc': '1',
		'origin': 'https://selfregistration.cowin.gov.in',
		'sec-fetch-site': 'cross-site',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://selfregistration.cowin.gov.in/',
		'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
		'if-none-match': 'W/"18839-1LvJ2peZ6lXrS5PWkV+8QwG8T/4"'
	}


	# Old headers
	# headers = CaseInsensitiveDict()
	# headers["accept"] = "application/json"
	# headers["Accept-Language"] = "hi_IN"

	try:
		resp = requests.request("GET", url, headers=headers, data=payload)

		if (resp.status_code == 403):
			print('Servers busy, retrying')
			# time.sleep(60)
			exit(1)

		centers = resp.json()['centers']

	except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError) as e:

		send_string = f"Program crashed due to {type(e).__name__}"
		print(send_string)
		exit(1)

	available = 0
	valid_centers = 0
	available_district_names = set()
	for centre in centers:

		pincode = centre['pincode']
		sessions = centre['sessions']

		if (302000 < pincode < 302999):

			valid_centers += 1

			for sess in sessions:

				min_age = sess['min_age_limit']
				available_capacity = sess['available_capacity']

				if (min_age < min_age_below and available_capacity >= min_available_capacity):
					available += available_capacity
					available_district_names.add(centre['name'])

	district_name = get_district_name(district_id)
	print(f"{district_name}: {valid_centers}/{len(centers)}", end=" | ")

	if (available > 0):

		available_district_names_str = " | ".join(available_district_names)
		send_string =  f'{available} vaccines in {district_name}: {available_district_names_str}'
		send_notification(send_string)

	return available

if __name__ == '__main__':

	print("Program started")

	day, month, _ = datetime.today().strftime('%d-%m-%Y').split('-')
	day = int(day)
	month = int(month)

	i = 0
	while (1):

		print(f"\rChecking for vaccine {i}", end=" | ")

		available = 0

		available = check_7_days_from(day, month, min_age_below, min_available_capacity, district_id=505)
		available += check_7_days_from(day, month, min_age_below, min_available_capacity, district_id=506)

		if (available > 0):
			generate_otp('8003115061')
			generate_otp('7895755566')
			break

		time.sleep(10)
		i += 1

		print('\t\t\t', end='\t')



