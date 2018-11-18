**Delete Custom Charges with the CloudCheckr API**

---

## Steps to Run


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install numpy, and requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html
3. Log in to CloudCheckr and create an Admin API access key.
4. Enter the CloudCheckr Account name of the payer account to line 48 in the variable payer_account_name.
5. Make sure that the add_charges.csv file is formatted correctly and in the same directory as the script.
6. Run python delete_custom_charges.py <cloudcheckr-admin-api-key>

---

## How the program works

It uses the [delete_custom_billing_charge_fixed](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#delete_custom_billing_charge_fixed) Admin API call to delete a fixed custom billing charge.


You can confirm the custom charges that were removed by going to the corresponding payer account and Cost -> AWS Partner Tools -> Configure -> Custom Billing Charges.

---

## How To Setup the Custom Charges

The program requires a specific input for the custom charges csv file in order to run. You should open up the added_charges.csv file and edit it to fit your team's requirements.

The first column should be the id of the fixed custom charge. The id can be found by using the [get_custom_billing_charges_v3](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_custom_billing_charges_v3) API call. It will also be saved as an output in the AddCustomCharges file.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 46 if required.
2. Only fixed one time custom charges specified in the input file added_charges.csv are to be removed.