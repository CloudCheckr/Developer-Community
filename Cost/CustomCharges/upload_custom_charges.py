import numpy as np
import json
import requests
import logging
import sys
logging.basicConfig(filename='upload_charges_logging_september.log',level=logging.INFO)


def load_custom_charges(custom_charges_file):

	custom_charges_dtype = [("Account", "U12"), 
							("Amount", "U36"),
							("startDate", "U10"),
							("endDate", "U10"),
							("description", "U70")]

	custom_charges = np.loadtxt(custom_charges_file, dtype=custom_charges_dtype, delimiter=",", skiprows=1)
	print(custom_charges)
	logging.info(custom_charges)
	print("\n")
	logging.info("\n")

	return custom_charges



def add_custom_fixed_charge(env, admin_api_key, startDate, endDate, amount, oneTime, description, account, payer_account_name):

	api_url = env + "api/billing.json/add_custom_billing_charge_fixed"

	fixedChargeData = json.dumps({"startDate": startDate, "endDate": endDate, "amount": amount, "oneTime": oneTime, "description": description, "accounts": [account], "use_account": payer_account_name})

	r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = fixedChargeData)


	if "Id" in r7.json():
		print("Added the custom charge " + description + " with the amount " + amount + " for the AWS Account " + account + " with a start date of " + startDate)
		print(r7.json())
		print("")
		logging.info("Added the custom charge " + description + " with the amount " + amount + " for the AWS Account " + account + " with a start date of " + startDate)
		logging.info(r7.json())
		logging.info("\n")
		return r7.json()["Id"]
	else:
		if (not (description is None)) and (not (account is None)):
			print("Custom charge " + description + " for account " + account + " failed")
			logging.info("Custom charge " + description + " for account " + account + " failed")
			logging.info(r7.json())
			logging.info("\n")
			print("\n")
			return None
		else:
			print("Custom charge " + description + " for account " + account + " failed")
			logging.info("Custom charge " + description + " for account " + account + " failed")
			logging.info(r7.json())
			logging.info("\n")
			print("\n")
			return None	

def cycle_custom_charges(env, admin_api_key, custom_charges, payerProjectId):

	if np.shape(custom_charges)[0] < 1:
		print("Custom Charges file too short")
		logging.info("Custom Charges file too short")
		return None
	charge_ids = np.array([])

	for i in np.arange(0, np.shape(custom_charges)[0]):
		charge_id = None
		if np.size(custom_charges[i]) != 5:
			charge_id = add_custom_fixed_charge(env, admin_api_key, custom_charges[i][2], custom_charges[i][3], custom_charges[i][1], "True", custom_charges[i][4], custom_charges[i][0], payerProjectId)
		else:
			print("Did NOT add custom charge of line " + str(i))
			logging.info("Did NOT add custom charge of line " + str(i))
		if not(charge_id is None):
			charge_ids = np.append(charge_ids, charge_id)

	return charge_ids


def main():
	try:
		admin_api_key = str(sys.argv[1])
	except IndexError:
		print("Must admin_api_key")
		return

	env = "https://api.cloudcheckr.com/"

	payer_account_name = "Payer Master Account"

	custom_charges_file = "custom_charges.csv"

	custom_charges = load_custom_charges(custom_charges_file)

	charge_ids = cycle_custom_charges(env, admin_api_key, custom_charges, payer_account_name)

	output_file = "added_charges.csv"

	np.savetxt(output_file, charge_ids, delimiter=",", newline="\n", fmt="%i")

	print("Saved custom charge id's added to " + output_file)
	logging.info("Saved custom charge id's added to " + output_file)



if __name__ == "__main__":
	main()