**Clear Account Families with the CloudCheckr API**

---

## Steps to Run


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install numpy, and requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html
3. Log in to CloudCheckr and create an Admin API access key.
4. Enter the CloudCheckr Account name of the payer account to line 59 in the variable payer_account_name.
5. Set up the payer's account family following the process below.
6. Run the below.

`
python clear_account_families.py <cloudcheckr-admin-api-key>
`
---

## How the program works

It uses the [get_account_family](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_account_family) Admin API call to get a list of all account families.

It uses the [delete_account_family](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#delete_account_family) Admin API call to delete all of the the account families except one that is specified.

You can confirm the account families were removed by going to Cost -> AWS Partner Tools -> Configure -> Account Families.

---

## How to Set Up Payer Account Family

For historical reasons, you can no longer delete all account families from a payer if some have already been created. It is
recommended that you create a single account family that contains the payer and name it Payer Account Family. This will
exist as a placeholder. You may have to manually remove the payer from an existing Account Family and create a new Account Family
with it. This new Account Family should be called Payer Account Family.

The script will download all Account Families and identify the account family with the payer by looking for an Account Family
with the name Payer Account Family. This account family will not be deleted and will be left as a placeholder.

Once the script completes you can then create new account families to fit your requirements. It is recommended not to delete the placeholder
account family until another account family is created.

If the Payer Account Family is not found, then the script will exit without deleting anything. Once the Payer Account Family is identified, the script will proceed with the deletion. You can change the name of the Payer Account Family by editing line 60.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 57 if required such is if you are using https://eu.cloudcheckr.com.
