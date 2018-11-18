**Add Fixed Custom Charges with the CloudCheckr API**

---

## Steps to Run


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install numpy, and requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html
3. Log in to CloudCheckr and create an Admin API access key.
4. Enter the CloudCheckr Account name of the payer account to line 90 in the variable payer_account_name.
4. Run python upload_custom_charges.py <cloudcheckr-admin-api-key>

---

## How the program works

It uses the [add_custom_billing_charge_fixed](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#add_custom_billing_charge_fixed) Admin API call to add a fixed custom billing charge.


You can view the custom charges that were added by going to the corresponding payer account and Cost -> AWS Partner Tools -> Configure -> Custom Billing Charges.

---

## How To Setup the Custom Charges

The program requires a specific input for the custom charges csv file in order to run. You should open up the custom_charges.csv file and edit it to fit your team's requirements. The first line is Account,Amount,startDate,endDate,Description.

The first column should be the twelve digit AWS Account Id of a payee account that is part of the payer that was specified. The second column should be the amount of the fixed custom charge. The third column should be the start date of the charge in year-month-date format (such as 2018-07-01). The last column is the end date of the charge is the same date format.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 88 if required.
2. Only fixed one time custom charges are to be added.