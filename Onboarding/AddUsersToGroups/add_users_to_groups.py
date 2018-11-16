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

def get_users_and_groups_permissions_template_input(file_name):

    add_users_to_groups_template_input = pd.read_csv(file_name)

    return add_users_to_groups_template_input


def get_users(env, admin_api_key):

    if check_invalid_env(env):
        return None

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

def get_groups(env, admin_api_key):
    """
    You have to check for and handle duplicate groups because historically CloudCheckr used to allow for duplicate group creation.
    """

    if check_invalid_env(env):
        return None, None

    api_url = env + "/api/account.json/get_groups"

    r7 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})

    groups_list = []
    groups_duplicate_list = []

    if "GroupNames" in r7.json():
        GroupNames = r7.json()["GroupNames"]
        for i in np.arange(0, len(GroupNames)):
            groups_list.append(GroupNames[i])
        for i in np.arange(0, len(GroupNames)):
            if groups_list.count(GroupNames[i]) > 1:
                groups_duplicate_list.append(GroupNames[i])
                log_information("Found duplicate group: " + GroupNames[i] + ". We recommend renaming it through the UI to remove duplicates.")

        return groups_list, groups_duplicate_list
    else:
        return groups_list, groups_duplicate_list

def get_user_id(env, admin_api_key, email):

    if check_invalid_env(env):
        return None

    api_url = env + "/api/account.json/get_users_v2"

    get_user_info = json.dumps({"email": email})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = get_user_info)

    if "user_permissions" in r7.json():
        user_permissions = r7.json()["user_permissions"]
        if len(user_permissions) > 0:
            if "id" in user_permissions[0]:
                return user_permissions[0]["id"]
            else:
                log_information("Could not find the user " + email)
                log_information(r7.json())
                return None
        else:
            log_information("Could not find the user " + email)
            log_information(r7.json())
            return None
    else:
        log_information("Could not find the user " + email)
        log_information(r7.json())
        return None

def get_groups_connector(admin_api_key, env):

    if check_invalid_env(env):
        return None

    api_url = env + "/api/account.json/get_groups_v2"

    get_user_info = json.dumps({})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = get_user_info)

    if "Groups" in r7.json():
        Groups = r7.json()["Groups"]
        if len(Groups) > 0:
            group_name_id_connector = np.zeros((len(Groups),2), dtype="U200")
            for i in np.arange(0, len(Groups)):
                if "Name" in Groups[i] and "Id" in Groups[i]:
                    group_name_id_connector[i][0] = Groups[i]["Name"]
                    group_name_id_connector[i][1] = Groups[i]["Id"]
                else:
                    log_information("Could not find name or id of group")
                    log_information(str(Groups[i]))
            return group_name_id_connector
        else:
            log_information("Could not find any Groups ")
            log_information(r7.json())
            return None
    else:
        log_information("Could not find any Groups")
        log_information(r7.json())
        return None


def get_group_id(group_name, group_name_id_connector):
    """
    Looks through the numpy array of a list of group names and their associated id.
    Then returns the group id for the inputted group name.
    """

    # TODO: vectorize this search to make it quicker
    for i in np.arange(0, np.shape(group_name_id_connector)[0]):
        if str(group_name_id_connector[i][0]) == str(group_name):
            return group_name_id_connector[i][1]
    return None


def add_user_to_group(admin_api_key, add_user_to_group_input_row, group_name_id_connector):
    env = add_user_to_group_input_row[0]

    if check_invalid_env(env):
        return None
    
    api_url = env + "/api/account.json/add_user_to_group"

    user_id = get_user_id(env, admin_api_key, add_user_to_group_input_row[1])

    if user_id is None:
        return None

    group_id = get_group_id(add_user_to_group_input_row[2], group_name_id_connector)

    if group_id is None:
        log_information("Could not find a group with the group name " + str(add_user_to_group_input_row[2]))
        return None    

    add_user_to_group_info = json.dumps({"user_ids": [user_id], "group_id": group_id})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = add_user_to_group_info)

    if "Message" in r7.json():
        if r7.json()["Message"] == "OK":
            log_information("Added the user " + add_user_to_group_input_row[1] + " to the group " + add_user_to_group_input_row[2])
            log_information(r7.json())
            return None
        else:
            log_information("Failed to add the user " + add_user_to_group_input_row[1] + " to the group " + add_user_to_group_input_row[2])
            log_information(r7.json())
            return None
    else:
        log_information("Failed to add the user " + add_user_to_group_input_row[1] + " to the group " + add_user_to_group_input_row[2])
        log_information(r7.json())
        return None


def cycle_add_users_to_groups(admin_api_key, add_users_to_groups_template_input, users_list, groups_list):

    log_information("Started adding users to groups")

    group_name_id_connector = get_groups_connector(admin_api_key, add_users_to_groups_template_input.iloc[0][0])
    # print(group_name_id_connector)
    if group_name_id_connector is None:
        log_information("Groups were not properly parsed, please contact Support")
        return

    for i in np.arange(0, np.shape(add_users_to_groups_template_input)[0]):
        if add_users_to_groups_template_input.iloc[i][1] in users_list:
            if add_users_to_groups_template_input.iloc[i][2] in groups_list:
                add_user_to_group(admin_api_key, add_users_to_groups_template_input.iloc[i], group_name_id_connector)
            else:
                log_information("The group " + add_users_to_groups_template_input.iloc[i][2] + " does not exist in this account, so the user " + add_users_to_groups_template_input.iloc[i][1] + " was not added to a group")
        else:
            log_information("The user " + add_users_to_groups_template_input.iloc[i][1] + " does not exist in this account, it was not added to a group")

    log_information("Finished adding users")
    return None

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
    file_name = "add_users_to_groups_input.csv"

    check_add_users_to_groups_input_file = Path(file_name)

    if check_add_users_to_groups_input_file.is_file():
        add_users_to_groups_template_input = get_users_and_groups_permissions_template_input(file_name)
    else:
        log_information("No add_users_to_groups_input.csv found. Please write file for input")
        return

    try:
        admin_api_key = sys.argv[1]
    except IndexError:
        print("Need admin_api_key in input")
        return

    # log_information(add_users_template_input)

    users_list = get_users(add_users_to_groups_template_input.iloc[0][0], admin_api_key)

    if users_list is None:
        return

    groups_list, groups_duplicate_list = get_groups(add_users_to_groups_template_input.iloc[0][0], admin_api_key)

    if groups_list is None:
        return

    if len(groups_duplicate_list) > 0:
        log_information("Please remove duplicate group names before proceeding.")
        return
    else:
        log_information("No duplicate groups found, please proceed.")

    cycle_add_users_to_groups(admin_api_key, add_users_to_groups_template_input, users_list, groups_list)


if __name__ == '__main__':
    main()
