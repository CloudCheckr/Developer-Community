import numpy as np
import json
import requests
import sys

# python delete_custom_charges.py 0000000000000000000000000000000000000000000000000000000000000000


def load_custom_charges(custom_charges_file):

	custom_charges_dtype = [("Id", "U36")]

	custom_charges = np.loadtxt(custom_charges_file, dtype="U36", delimiter=",")
	# print(custom_charges)

	return custom_charges


def delete_custom_fixed_charge(env, admin_api_key,custom_charge_id, payer_account_name):

	api_url = env + "api/billing.json/delete_custom_billing_charge"

	chargeData = json.dumps({"Id": custom_charge_id, "use_account": payer_account_name})

	r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = chargeData)

	print("Deleted the custom charge " + str(custom_charge_id))
	print(r7.json())

def cycle_custom_charges(env, admin_api_key, custom_charges, payer_account_name):


	charge_ids = np.array([])

	for i in np.arange(0, np.shape(custom_charges)[0]):
		charge_id = delete_custom_fixed_charge(env, admin_api_key,custom_charges[i], payer_account_name)


def main():
	try:
		admin_api_key = str(sys.argv[1])
	except IndexError:
		print("Must admin_api_key")
		return

	env = "https://api.cloudcheckr.com/"

	payer_account_name = "Payer Master Account"

	custom_charges_file = "added_charges.csv"

	custom_charges = load_custom_charges(custom_charges_file)

	charge_ids = cycle_custom_charges(env, admin_api_key, custom_charges, payer_account_name)



if __name__ == "__main__":
	main()