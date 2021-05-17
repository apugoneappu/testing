"""
My first application
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from utils.otp import *
import requests
import json
from hashlib import sha256

class BookMySlot(toga.App):

	def startup(self):
		"""
		Construct and show the Toga application.

		Usually, you would add your application to a main content box.
		We then create a main window (with a name matching the app), and
		show the main window.
		"""
		main_box = toga.Box(style=Pack(direction=COLUMN))

		mobile_number_label = toga.Label(
			'Mobile Number: ',
			style=Pack(padding=(0, 5))
		)
		self.mobile_number_input = toga.TextInput(style=Pack(flex=1))
		mobile_number_box = toga.Box(style=Pack(direction=ROW, padding=5))
		mobile_number_box.add(mobile_number_label)
		mobile_number_box.add(self.mobile_number_input)

		otp_button = toga.Button(
			'Get OTP',
			on_press=self.send_otp,
			style=Pack(padding=5)
		)
		print(otp_button)

		# otp
		otp_label = toga.Label(
			'OTP: ',
			style=Pack(padding=(0, 5))
		)
		self.otp_input = toga.TextInput(style=Pack(flex=1), on_change=self.validate_otp)
		otp_box = toga.Box(style=Pack(direction=ROW, padding=5))
		otp_box.add(otp_label)
		otp_box.add(self.otp_input)

		# pincode
		pincode_lable = toga.Label(
			'Pincode: ',
			style=Pack(padding=(0, 5))
		)
		self.pincode_input = toga.TextInput(style=Pack(flex=1))
		pincode_box = toga.Box(style=Pack(direction=ROW, padding=5))
		pincode_box.add(pincode_lable)
		pincode_box.add(self.pincode_input)

		# state
		state_label = toga.Label(
			'State: ',
			style=Pack(padding=(0, 5))
		)
		self.state_input = toga.Selection(items=['bob', 'jim', 'lilly'])
		state_box = toga.Box(style=Pack(direction=ROW, padding=5))
		state_box.add(state_label)
		state_box.add(self.state_input)

		# district
		district_label = toga.Label(
			'District: ',
			style=Pack(padding=(0, 5))
		)
		self.district_input = toga.Selection(items=['bob', 'jim', 'lilly'])
		district_box = toga.Box(style=Pack(direction=ROW, padding=5))
		district_box.add(district_label)
		district_box.add(self.district_input)

		# start button
		start_button = toga.Button(
			'Start',
			on_press=self.say_hello,
			style=Pack(padding=5)
		)

		# adding boxes to window
		main_box.add(mobile_number_box)
		main_box.add(otp_button)
		main_box.add(otp_box)
		main_box.add(pincode_box)
		main_box.add(state_box)
		main_box.add(district_box)
		main_box.add(start_button)

		self.main_window = toga.MainWindow(title=self.formal_name)
		self.main_window.content = main_box
		self.main_window.show()

	def say_hello(self, widget):
		print("Hello", self.mobile_number_input.value)

	def send_otp(self, widget):
		send_payload['mobile'] = self.mobile_number_input.value

		response = requests.request("POST", send_url, headers=send_headers, data=json.dumps(send_payload))

		status = response.status_code

		if status == 200:
			data = response.json().get('txnId', '')
			msg = f'txnID is {data}'
			self.txnId = data
		elif status == 400:
			data = ''
			msg = response.json().get('error', '')
		else:
			data = ''
			msg = response.raw

		print(msg)

	def validate_otp(self, widget):
		if len(self.otp_input.value) == 6:
			validate_payload['otp'] = str(sha256(str(self.otp_input.value).encode('utf-8')).hexdigest())
			validate_payload['txnId'] = str(self.txnId)

			response = requests.request("POST", validate_url, headers=validate_headers, data=json.dumps(validate_payload))

			status = response.status_code

			if status == 200:
				data = response.json().get('token', '')
				msg = f'token is {data}'
			elif status == 400:
				data = ''
				msg = response.json().get('error', '')
			else:
				data = ''
				msg = response.raw

			print(msg)

def main():
	return BookMySlot()
