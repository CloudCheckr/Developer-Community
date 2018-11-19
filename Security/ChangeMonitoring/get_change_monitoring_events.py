import requests
import json
import numpy as np
import sys

"""
This python script is used to add cost alerts to all non mav AWS accounts
python get_change_monitoring.py 0000000000000000000000000000000000000000000000000000000000000000
"""

def log_information(log_string):
    print(log_string)


def get_changes(admin_api_key, env, account_name):

    if check_invalid_env(env):
        return

    api_url = env + "/api/change_monitoring.json/get_changes"

    change_monitoring_info = json.dumps({"use_account": account_name})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = change_monitoring_info)

    print(r7.json())


def check_invalid_env(env):
    """
    This will check for an invalid enviroment. Currently it will only check for api, eu, au, or gov.
    If you are using a standalone environment, then you MUST add that to this function
    """

    Enviroments = ["https://api.cloudcheckr.com", "https://eu.cloudcheckr.com", "https://au.cloudcheckr.com", "https://gov.cloudcheckr.com", "https://qa.cloudcheckr.com"]


    if not(env in Enviroments):
        log_information("The environment " + str(env) + " is not valid. If this is a standalone environment, please add the url to the check_invalid_env function.")
        return True
    return False


def main():
    try:
        admin_api_key = str(sys.argv[1])
    except IndexError:
        print("Must include non-admin API key of account that you want to pull via")
        return

    env = "https://api.cloudcheckr.com"

    account_name = "Account Name Here"


    get_changes(admin_api_key, env, account_name)


if __name__ == '__main__':
    main()
