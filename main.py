import json
import argparse
import sys
import time
import pandas as pd

from schedule import Schedule
from otp import OTP
from beneficiaries import Beneficiaries
from appointment import Appointment

import logging
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

parser = argparse.ArgumentParser(description="Vaccination booking script")

#add the arguments
parser.add_argument("--config", '-c', type=str, help="relative path of config file")
args = parser.parse_args()

with open(args.config) as f:
  config = json.load(f)

otp = OTP()
txnId = otp.send_otp(config['mobile'])

otp_recv = input('Please enter OTP: ')
token = otp.validate_otp(otp_recv, txnId)
if (token == ''):
	sys.exit('Invalid OTP!')

bf = Beneficiaries(config['names'])
ap = Appointment(config['pincode_from'], config['my_pincode'], config['pincode_to'])
sched = Schedule()

while (token):
	num_44_or_less, num_45_or_more, bfs = bf.get_beneficiaries(token)

	if len(bfs) == 0:
		break
	
	slots = []
	for d_code in config['district_ids']:
		slots.append(ap.find_slots(d_code))

	slots_comb = pd.concat(slots)
	slots_comb.drop_duplicates(inplace=True, ignore_index=True)

	appointments = ap.find_suitable_slots(slots_comb, num_44_or_less, num_45_or_more)

	sched.book_vaccine(token, bfs, appointments)

	time.sleep(3.5)