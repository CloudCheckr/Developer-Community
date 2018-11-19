import requests
import json
import numpy as np
import sys

"""
This python script is used to get all ec2 instances
python3 get_ec2_instances.py 0000000000000000000000000000000000000000000000000000000000000000
"""

def get_token_ec2_instances(admin_api_key, env, account_name, i, next_token):

    # if first time the method is called
    if i == 0:
        i += 1
        api_url = env + "/api/inventory.json/get_resources_ec2_details_v4?access_key=" + admin_api_key + "&use_account=" + account_name
        r7 = requests.get(api_url)
        if "Ec2Instances" in r7.json():
            print(r7.json()["Ec2Instances"])
            if "HasNext" in r7.json():
                if r7.json()["HasNext"] == True:
                    next_token = r7.json()["NextToken"]
                    return i, False, next_token
                else:
                    return i, True, "0000"
            else:
                print("Could not find HasNext value")
        else:
            print("Could not find any instances")
            print(r7.json())
    else:
        i += 1
        api_url = env + "/api/inventory.json/get_resources_ec2_details_v4?access_key=" + admin_api_key + "&use_account=" + account_name + "&next_token=" + next_token
        r7 = requests.get(api_url)
        if "Ec2Instances" in r7.json():
            print(r7.json()["Ec2Instances"])
            if "HasNext" in r7.json():
                if r7.json()["HasNext"] == True:
                    next_token = r7.json()["NextToken"]
                    return i, False, next_token
                else:
                    return i, True, "0000"
            else:
                print("Could not find HasNext value")
        else:
            print("Could not find any instances")
            print(r7.json())

def get_ec2_instances(admin_api_key, env, account_name):

    if check_invalid_env(env):
        return

    finish = False
    i = 0
    next_token = "00000"

    while finish == False:
        i, finish, next_token = get_token_ec2_instances(admin_api_key, env, account_name, i, next_token)


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

    # enter name of account here
    account_name = "Account Name Here"

    get_ec2_instances(admin_api_key, env, account_name)


if __name__ == '__main__':
    main()
