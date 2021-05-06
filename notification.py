import requests

def send_notification(string):

	print(string)
	NOTIF_URL = "https://maker.ifttt.com/trigger/vaccine_available/with/key/bx-gv6c4m0BUSKu_l0a0gu"
	notif_resp = requests.get(NOTIF_URL, params={"value1": string})