import requests

class UpdateChecker():
	"""Closes the program if the current version is not equal to the latest version
	"""

	def __init__(self) -> None:

		self.version_url = 'https://bookmyslot-version.herokuapp.com/'
		self.vaccine_names_url = 'https://bookmyslot-version.herokuapp.com/vaccine_names'

	def get_latest_version(self):

		response = requests.get(self.version_url)

		latest = ''
		if response.status_code == 200:
			latest = response.text	

		return latest
	
	def get_vaccine_names(self):

		response = requests.get(self.vaccine_names_url)

		latest = ''
		if response.status_code == 200:
			latest = response.text	

		return latest


if __name__ == '__main__':
	uc = UpdateChecker()
	v = uc.get_latest_version()
	print(v)
	