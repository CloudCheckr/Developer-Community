import requests
import json
import pandas as pd
import numpy as np
import sys
import logging
from pathlib import Path
logging.basicConfig(filename='logging_for_creating_groups.log',level=logging.INFO)

"""
This python script is used to create groups based on the create_groups_input.csv file.
python3 create_groups.py 0000000000000000000000000000000000000000000000000000000000000000
"""

def log_information(log_string):
    logging.info(log_string)
    print(log_string)


def get_group_names_template_input(file_name):

    group_names_template_input = pd.read_csv(file_name)

    return group_names_template_input


def write_groups_created(groups_output, group_recorder):
    np.savetxt(groups_output, group_recorder, fmt="%s", delimiter=",", newline="\n")

def create_group(admin_api_key, env, group_name):


    if check_invalid_env(env):
        return None
    
    api_url = env + "/api/account.json/create_group"

    group_info = json.dumps({"name": group_name})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = group_info)

    group_id = None

    if "group_id" in r7.json():
        group_id = r7.json()["group_id"]
        log_information("Created the Group: " + group_name + " with id: " + str(group_id))
        log_information(r7.json())
    else:
        log_information("Failed to create the group: " + str(group_name))
        log_information(r7.json())

    return group_id

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

def cycle_create_groups(admin_api_key, group_names_template_input, groups_list):

    group_recorder = np.zeros((np.shape(group_names_template_input)[0] + 1, 2), dtype="U200")
    group_recorder[0][0] = "GroupName"
    group_recorder[0][1] = "group_id"

    for i in np.arange(0, np.shape(group_names_template_input)[0]):
        if not(group_names_template_input.iloc[i][1] in groups_list):
            group_id = create_group(admin_api_key, group_names_template_input.iloc[i][0], group_names_template_input.iloc[i][1])
            if group_id is None:
                group_id = "Failed"
            else:
                groups_list.append(group_names_template_input.iloc[i][1])
                group_recorder[i + 1][0] = str(group_names_template_input.iloc[i][1])
                group_recorder[i + 1][1] = str(group_id)
        else:
            log_information("A group with the name " + group_names_template_input.iloc[i][1] + " has already been created. Please rename it")

    write_groups_created("GroupsCreated.csv", group_recorder)


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
    file_name = "create_groups_input.csv"

    check_groups_input_template = Path(file_name)

    if check_groups_input_template.is_file():
        group_names_template_input = get_group_names_template_input(file_name)
    else:
        log_information("No group_permissions_input.csv found. Please write file for input")
        return

    try:
        admin_api_key = sys.argv[1]
    except IndexError:
        print("Need admin_api_key in input")
        return

    groups_list, groups_duplicate_list = get_groups(group_names_template_input.iloc[0][0], admin_api_key)

    if groups_list is None:
        return

    if len(groups_duplicate_list) > 0:
        log_information("Please remove duplicate group names before proceeding.")
        return
    else:
        log_information("No duplicate groups found, please proceed.")  

    # print(groups_list)

    cycle_create_groups(admin_api_key, group_names_template_input, groups_list)


if __name__ == '__main__':
    main()