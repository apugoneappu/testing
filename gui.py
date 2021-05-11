import tkinter as tk
from main_gui import Main
from functools import partial

import requests
import json
from hashlib import sha256
import logging

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


class OTP():
	def __init__(self) -> None:

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
			msg = data
		elif status == 400:
			data = ''
			msg = response.json().get('error', '')
		else:
			data = ''
			msg = response.raw

		logger.info(f'{status}: {msg}')
		return data

	def validate_otp(self, otp: str, txnId: str) -> str:

		self.validate_payload['otp'] = str(sha256(str(otp).encode('utf-8')).hexdigest())
		self.validate_payload['txnId'] = str(txnId)

		response = requests.request("POST", self.validate_url, headers=self.validate_headers, data=json.dumps(self.validate_payload))

		status = response.status_code

		if status == 200:
			data = response.json().get('token', '')
			msg = data
		elif status == 400:
			data = ''
			msg = response.json().get('error', '')
		else:
			data = ''
			msg = response.raw

		logger.info(f'{status}: {msg}')
		return data



class GUI():

	def __init__(self) -> None:

		self.otp = OTP()
		self.logs = ''

		self.window = tk.Tk()
		self.window.title('BookMySlot')

		self.window.geometry("700x500")

		self.window.rowconfigure([0,1,2,3,4,5], weight=1)
		self.window.rowconfigure(6, weight=2)
		self.window.columnconfigure(0, weight=1)

		################ APP NAME #################

		self.frame_app_name = tk.Frame(master=self.window)
		self.frame_app_name.grid(row=0, column=0, sticky='news')

		self.frame_app_name.rowconfigure(0, weight=1)
		self.frame_app_name.columnconfigure(0, weight=1)

		self.label_app_name = tk.Label(master=self.frame_app_name, text='BookMySlot: Covid Vaccine Booking')
		self.label_app_name.grid(row=0, column=0, sticky='news')

		################ MOBILE #################

		self.frame_mobile = tk.Frame(master=self.window)
		self.frame_mobile.grid(row=1, column=0, sticky='news')

		self.frame_mobile.rowconfigure(0, weight=1)
		self.frame_mobile.columnconfigure(0, weight=2) #label
		self.frame_mobile.columnconfigure(1, weight=5) #entry
		self.frame_mobile.columnconfigure(2, weight=2) #button

		self.label_mobile = tk.Label(master=self.frame_mobile , text='Mobile number')
		self.label_mobile.grid(row=0, column=0, sticky='news')

		self.entry_mobile = tk.Entry(master=self.frame_mobile, validate='focus')
		self.entry_mobile['validatecommand'] = (self.entry_mobile.register(self.check_number_format), '%P')
		self.entry_mobile.grid(row=0, column=1, sticky='news')

		self.button_mobile = tk.Button(master=self.frame_mobile, text='Get OTP', command=self.get_otp_callback)
		self.button_mobile.grid(row=0, column=2, sticky='news')

		################ OTP #################

		self.frame_otp = tk.Frame(master=self.window)
		self.frame_otp.grid(row=2, column=0, sticky='news')

		self.frame_otp.rowconfigure(0, weight=1)
		self.frame_otp.columnconfigure(0, weight=2) #label
		self.frame_otp.columnconfigure(1, weight=7) #entry

		self.label_otp = tk.Label(master=self.frame_otp , text='OTP number')
		self.label_otp.grid(row=0, column=0, sticky='news')

		self.entry_otp = tk.Entry(master=self.frame_otp)
		self.entry_otp.grid(row=0, column=1, sticky='news')

		################ Pincode #################

		self.frame_pincode = tk.Frame(master=self.window)
		self.frame_pincode.grid(row=3, column=0, sticky='news')

		self.frame_pincode.rowconfigure(0, weight=1)
		self.frame_pincode.columnconfigure([0,2,4], weight=2) #labels
		self.frame_pincode.columnconfigure([1,3,5], weight=7) #entries

		self.label_pincode_from = tk.Label(master=self.frame_pincode , text='Pincode from')
		self.label_pincode_from.grid(row=0, column=0, sticky='news')

		self.entry_pincode_from = tk.Entry(master=self.frame_pincode)
		self.entry_pincode_from.grid(row=0, column=1, sticky='news')

		self.label_pincode = tk.Label(master=self.frame_pincode, text='Pincode')
		self.label_pincode.grid(row=0, column=2, sticky='news')

		self.entry_pincode = tk.Entry(master=self.frame_pincode)
		self.entry_pincode.grid(row=0, column=3, sticky='news')

		self.label_pincode_to = tk.Label(master=self.frame_pincode , text='Pincode to')
		self.label_pincode_to.grid(row=0, column=4, sticky='news')

		self.entry_pincode_to = tk.Entry(master=self.frame_pincode)
		self.entry_pincode_to.grid(row=0, column=5, sticky='news')

		################ Names #################

		self.frame_names = tk.Frame(master=self.window)
		self.frame_names.grid(row=4, column=0, sticky='news')

		self.frame_names.rowconfigure(0, weight=1)
		self.frame_names.columnconfigure(0, weight=2) #label
		self.frame_names.columnconfigure(1, weight=7) #entry

		self.label_names = tk.Label(master=self.frame_names , text='Enter names (comma separated)')
		self.label_names.grid(row=0, column=0, sticky='news')

		self.entry_names = tk.Entry(master=self.frame_names)
		self.entry_names.grid(row=0, column=1, sticky='news')

		################ Captcha #################

		self.frame_captcha = tk.Frame(master=self.window)
		self.frame_captcha.grid(row=5, column=0, sticky='news')

		self.frame_captcha.rowconfigure([0,1], weight=1) 
		self.frame_captcha.columnconfigure(0, weight=2) # frameleft - label, entry
		self.frame_captcha.columnconfigure(1, weight=7) #label

		self.label_captcha = tk.Label(master=self.frame_captcha, text='Enter captcha')
		self.label_captcha.grid(row=0, column=0, rowspan=1, columnspan=1)

		self.entry_captcha = tk.Entry(master=self.frame_captcha)
		self.entry_captcha.grid(row=1, column=0, rowspan=1, columnspan=1)

		# Image right
		from PIL import ImageTk, Image
		load = Image.open("output.png")
		self.img = ImageTk.PhotoImage(load)
		self.label_image = tk.Label(master=self.frame_captcha, image=self.img)
		self.label_image.image = self.img
		self.label_image.grid(row=0, column=1, sticky='news', rowspan=2, columnspan=1)

		################ Output #################
		self.frame_output = tk.Frame(master=self.window)
		self.frame_output.grid(row=6, column=0, sticky='new')

		self.frame_output.rowconfigure(0, weight=1)
		self.frame_output.rowconfigure(1, weight=10)
		self.frame_output.columnconfigure(0, weight=10)

		self.label_output = tk.Label(master=self.frame_output, text='Output logs', bg='red')
		self.label_output.grid(row=0, column=0)

		self.logs = tk.StringVar()
		self.label_output = tk.Label(master=self.frame_output, text='', bg='blue')
		self.label_output['textvariable'] = self.logs
		self.label_output.grid(row=1, column=0)

	
	def check_number_format(self, input_str: str):

		white_removed = input_str.replace(' ', '')
		ret = len(white_removed) == 10 and white_removed.isdecimal()
		if ret:
			self.entry_mobile.configure(background='green')
			self.button_mobile['state'] = 'normal'
		else:
			self.entry_mobile.configure(background='red')
			self.button_mobile['state'] = 'disabled'
		print(ret)
		return ret
	
	def get_otp_callback(self):

		mobile = self.entry_mobile.get()
		mobile = int(mobile)

		self.tnxId = self.otp.send_otp(mobile)
		self.log(f'tnxId: {self.tnxId}')

	def log(self, addition):

		self.logs.set(self.logs.get() + '\n' + addition)

gui = GUI()
gui.window.mainloop()