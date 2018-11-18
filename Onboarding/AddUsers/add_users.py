import requests
import json
import pandas as pd
import numpy as np
import sys
import logging
from pathlib import Path
logging.basicConfig(filename='logging_for_adding_users.log',level=logging.INFO)

"""
This python script is used to add users based on the add_users_input.csv file.
python3 add_users.py 0000000000000000000000000000000000000000000000000000000000000000
"""

def log_information(log_string):
    logging.info(log_string)
    print(log_string)


def write_users_created(users_output, users_recorder):
    np.savetxt(users_output, users_recorder, fmt="%s", delimiter=",", newline="\n")


def get_users_permissions_template_input(file_name):

    add_users_template_input = pd.read_csv(file_name)

    return add_users_template_input


def get_users(env, admin_api_key):

    if check_invalid_env(env):
        return

    api_url = env + "/api/account.json/get_users"

    r7 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})

    users_list = []

    if "users_and_accounts" in r7.json():
        users_and_accounts = r7.json()["users_and_accounts"]
        for i in np.arange(0, len(users_and_accounts)):
            users_list.append(users_and_accounts[i]["username"])

        return users_list
    else:
        return users_list


def add_user(admin_api_key, add_user_input_row):
    env = add_user_input_row[0]

    if check_invalid_env(env):
        return None
    
    api_url = env + "/api/account.json/add_user"

    available_roles = ["Administrator", "User", "BasicPlusUser", "BasicUser", "ReadonlyUser"]

    if not(add_user_input_row[2] in available_roles):
        log_information("The user " + add_user_input_row[1] + " was not added because the role " + add_user_input_row[2] + " does not exist.")
        return None

    add_user_info = json.dumps({"email": add_user_input_row[1], "user_role": add_user_input_row[2]})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = add_user_info)

    if "CreationStatuses" in r7.json():
        log_information("Added the user " + add_user_input_row[1] + " with the role " + add_user_input_row[2])
        log_information(r7.json())
        return add_user_input_row[1]
    else:
        log_information("Failed to add the user " + add_user_input_row[1])
        log_information(r7.json())
        return None


def cycle_add_users(admin_api_key, add_users_template_input, users_list):

    users_recorder = np.zeros((np.shape(add_users_template_input)[0]+1), dtype="U200")
    users_recorder[0] = "Users"
    log_information("Started adding users")

    for i in np.arange(0, np.shape(add_users_template_input)[0]):
        if not(add_users_template_input.iloc[i][1] in users_list):
            new_user = add_user(admin_api_key, add_users_template_input.iloc[i])
            if not(new_user is None):
                users_recorder[i + 1] = new_user
                users_list.append(new_user)
            else:
                log_information("The user " + str(add_users_template_input.iloc[i][1]) + " was not added successfully")
        else:
            log_information("The user " + add_users_template_input.iloc[i][1] + " already exists in this account, so it was not added")
        log_information("")

    log_information("Finished adding users")
    return users_recorder

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
    file_name = "add_users_input.csv"

    check_add_users_input_file = Path(file_name)

    if check_add_users_input_file.is_file():
        add_users_template_input = get_users_permissions_template_input(file_name)
    else:
        log_information("No add_users_input.csv found. Please write file for input")
        return

    try:
        admin_api_key = sys.argv[1]
    except IndexError:
        print("Need admin_api_key in input")
        return

    # log_information(add_users_template_input)

    users_list = get_users(add_users_template_input.iloc[0][0], admin_api_key)

    if users_list is None:
        return

    users_recorder = cycle_add_users(admin_api_key, add_users_template_input, users_list)

    write_users_created("UsersCreated.csv", users_recorder)


if __name__ == '__main__':
    main()
