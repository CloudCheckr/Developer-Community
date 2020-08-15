import requests
import json
import pandas as pd
import numpy as np
import sys
import logging


"""
1) This python script is used to delete accounts based on the list of accounts provided in a csv file named 'accounts_list'.  Please see example datafile for formatting.
2) For the data file, please define 2 columns:
    Column 1: the API URI for your region in CloudCheckr
        Valid regions:
            https://api.cloudcheckr.com
            https://eu.cloudcheckr.com
            https://au.cloudcheckr.com
            https://gov.cloudcheckr.com
    Column 2: the corresponding account name of the account you wish to be deleted (as it appears in the CloudCheckr landing page)
    Note:  The first row is for column names
3) To call this script, use the following: python3 delete_accounts.py <admin level access key>
4) Please ensure that this file is in the same folder/directory as the data file.
"""


logging.basicConfig(filename='logging_for_deleting_accounts.log',level=logging.INFO)

def get_accounts_input(file_name):
    accounts_list = pd.read_csv(file_name)
    return accounts_list

def delete_account(env, admin_api_key, account_name):
    api_url = env + "/api/account.json/delete_account"
    delete_user_info = json.dumps({"account_name": account_name})

    try:
        r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = delete_user_info)
        if r7.status_code == 200:
            logging.info("Success: {}, request to '{}' with parameters '{}'".format(r7.status_code, api_url, delete_user_info))

        else:
            # If an error is logged as a WARNING due to this else clause, an error code should be returned. This code can be looked up by CloudCheckr Support to assist with debugging.
            logging.warning("Request to {} Failed: {}, Request parameters '{}'\n{}".format(api_url, r7.status_code, delete_user_info, r7.json()))

    except requests.exceptions.RequestException as e:
        logging.critical('Request Exception: {}'.format(e))

def cycle_delete_accounts(admin_api_key, accounts_list):
    logging.info("Started deleting accounts")
    for i in np.arange(0, np.shape(accounts_list)[0]):
        delete_account(accounts_list.iloc[i][0], admin_api_key, accounts_list.iloc[i][1])

    logging.info("Finished deleting accounts")
    return 1

def main():
    file_name = "accounts_list.csv"
    accounts_input = get_accounts_input(file_name)

    try:
        admin_api_key = sys.argv[1]
    except IndexError:
        print("Need admin_api_key in input")
        sys.exit()

    cycle_delete_accounts(admin_api_key, accounts_input)


if __name__ == '__main__':
    main()
