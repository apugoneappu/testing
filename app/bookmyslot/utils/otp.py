send_url = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"
send_payload = {
	"secret": "U2FsdGVkX1/XpFGbdwjsUeP/PjBl0AP4QVlJDt8t+6PPaiJFMtlmcUeciyb+XZzQh6Jm6WlZM+nRD/CY6/SpVg==",
	"mobile": 7384488341
}
send_headers = {
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

validate_url = "https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp"
validate_payload = {
	"otp": "89b4e7cc1899427a932ddeef68a321238098beb02557f6044f6cd81b1cdc4e73",
	"txnId": "c9f55e11-5518-4454-b3a9-db336393c317"
}
validate_headers = {
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
