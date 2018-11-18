import requests
import json
import pandas as pd
import numpy as np
import sys
import logging
from pathlib import Path
logging.basicConfig(filename='logging_for_get_access_control_list.log',level=logging.INFO)

"""
This python script is used to get the permissions of the Permission Template and output it as a csv file.
The input is the permission_template_input.csv file and an admin api key.
python3 get_access_control_list_per_group.py 0000000000000000000000000000000000000000000000000000000000000000
"""

def log_information(log_string):
    logging.info(log_string)
    print(log_string)

def get_permission_template_input(file_name):

    permission_template_input = pd.read_csv(file_name)

    return permission_template_input


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


def get_groups_connector(admin_api_key, env):


    if check_invalid_env(env):
        return None

    api_url = env + "/api/account.json/get_groups_v2"

    get_group_info = json.dumps({})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = get_group_info)

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


def get_acl_permission(acl, complete_acl_list):
    """
    This uses numpy's vectorized operations to quickly match the acl returned from the API, to
    the complete list of acls to get the description.
    """

    index = -1 

    where_arrays = np.where(acl == complete_acl_list[:,0])

    try:
        index = where_arrays[0][0]
        # print(complete_acl_list[index])
        return complete_acl_list[index][1], complete_acl_list[index][2]
    except IndexError:
        return "Unknown", "Unknown"

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


def get_permissions_for_group_and_account(env, admin_api_key, group_name, account_name, group_name_id_connector, complete_acl_list):


    if check_invalid_env(env):
        return None

    group_id = get_group_id(group_name, group_name_id_connector)

    if group_id is None:
        log_information("Could not find a group with the group name " + str(group_name))
        return None    

    api_url = env + "/api/account.json/get_access_control_list_per_group?group_id=" + group_id + "&use_account=" + account_name

    r7 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})

    if "Acls" in r7.json():
        Acls = r7.json()["Acls"]
    else:
        log_information("Could not find acls for group: " + str(group_id) + " and account " + str(account_name))
        return None

    AccountPermissions = np.zeros((np.shape(Acls)[0]+1,3), dtype="U86")
    AccountPermissions[0][0] = "Acls"
    AccountPermissions[0][1] = "Section"
    AccountPermissions[0][2] = "Permission"
    for i in np.arange(1, np.shape(AccountPermissions)[0]):
        AccountPermissions[i][0] = Acls[i-1]["Id"]
        permission = get_acl_permission(Acls[i-1]["Id"], complete_acl_list)
        AccountPermissions[i][1] = permission[0]
        AccountPermissions[i][2] = permission[1]

    return AccountPermissions


def get_complete_acl_list(admin_api_key, env):
    """
    Gets all of the access control lists from the API one time. Then uses this data to specify which permissions
    are being granted later on.
    """

    if check_invalid_env(env):
        return None

    api_url = env + "/api/account.json/get_access_control_list"

    get_acl_info = json.dumps({})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = get_acl_info)

    if "responseModel" in r7.json():
        responseModel = r7.json()["responseModel"]

        complete_acl_list = np.zeros((np.shape(responseModel)[0],3), dtype=("U100"))
        for i in np.arange(0, np.shape(complete_acl_list)[0]):
            if "Id" in responseModel[i] and "Section" in responseModel[i] and "Name" in responseModel[i]:
                complete_acl_list[i][0] = responseModel[i]["Id"]
                complete_acl_list[i][1] = responseModel[i]["Section"]
                if len(str(complete_acl_list[i][1])) == 0:
                    complete_acl_list[i][1] = "Generic"
                complete_acl_list[i][2] = responseModel[i]["Name"]
            else:
                log_information("Could not find a particlar acl info, so it was skipped")
        return complete_acl_list

    else:
        log_information("Could not get any acls from API")
        log_information(r7.json())
        return None


def get_account_names_of_template_group(admin_api_key, env, group_id):
    """
    This pulls the names of the FOUR accounts that will serve as permission templates.
    If an account type has already been used for the template, then that account in the group will be SKIPPED.
    Returns the names of the 4 accounts.
    If an account type is not included, then it will return None. 
    """

    if check_invalid_env(env):
        return None

    api_url = env + "/api/account.json/get_accounts_by_group"

    get_accounts_group_info = json.dumps({"group_id": group_id})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = get_accounts_group_info)

    # print(r7.json())

    account_types_counter = np.zeros(4, dtype=np.int64) # used to keep track of which account types already have permissions
    account_type_names = [None, None, None, None]

    if "Projects" in r7.json():
        Projects = r7.json()["Projects"]
        if not(np.shape(Projects)[0] < 1):
            for i in np.arange(0, np.shape(Projects)[0]):
                if "Provider" in Projects[i] and "Type" in Projects[i] and "Name" in Projects[i]:
                    if Projects[i]["Provider"] == "Amazon Web Services":
                        if Projects[i]["Type"] == "General":
                            if account_types_counter[0] < 1:
                                account_type_names[0] = Projects[i]["Name"]
                                account_types_counter[0] += 1
                                log_information("The account " + str(account_type_names[0]) + " was used as the permission template for AWS Accounts.")
                            else:
                                log_information("The account " + Projects[i]["Name"] + " was skipped because there is already an AWS Account used in the template.")
                        else:
                            if Projects[i]["Type"] == "MultiView":
                                if account_types_counter[1] < 1:
                                    account_type_names[1] = Projects[i]["Name"]
                                    account_types_counter[1] += 1
                                    log_information("The account " + str(account_type_names[1]) + " was used as the permission template for AWS MAV Accounts.")
                                else:
                                    log_information("The account " + Projects[i]["Name"] + " was skipped because there is already an AWS MAV Account used in the template.")
                            else:
                                log_information("CloudCheckr is returning an AWS Account type that is not a MAV or a General account. Please contact support")
                    else:
                        if Projects[i]["Provider"] == "Microsoft Azure":
                            if Projects[i]["Type"] == "General":
                                if account_types_counter[2] < 1:
                                    account_type_names[2] = Projects[i]["Name"]
                                    account_types_counter[2] += 1
                                    log_information("The account " + str(account_type_names[2]) + " was used as the permission template for Azure Accounts.")
                                else:
                                    log_information("The account " + Projects[i]["Name"] + " was skipped because there is already an Azure Account used in the template.")
                            else:
                                if Projects[i]["Type"] == "MultiView":
                                    if account_types_counter[3] < 1:
                                        account_type_names[3] = Projects[i]["Name"]
                                        account_types_counter[3] += 1
                                        log_information("The account " + str(account_type_names[3]) + " was used as the permission template for Azure MAV Accounts.")
                                    else:
                                        log_information("The account " + Projects[i]["Name"] + " was skipped because there is already an Azure MAV Account used in the template.")
                                else:
                                    log_information("CloudCheckr is returning an Azure Account type that is not a MAV or a General account. Please contact support")
                        else:
                            log_information("CloudCheckr is returning an Account type that is not a Microsoft Azure or Amazon Web Services. Please contact support")
                else:
                    log_information("Could not find provider or type in the group with group_id: " + str(group_id) + " and project " + str(Projects[i]))
                    log_information(r7.json())
        else:
            log_information("Could not find any accounts in the group with group_id: " + str(group_id))
            log_information(r7.json())
    else:
        log_information("Could not get the accounts in the group with group_id: " + str(group_id))
        log_information(r7.json())

    return account_type_names[0], account_type_names[1], account_type_names[2], account_type_names[3]

def write_account_permissions(account_type, account_permissions):
    np.savetxt(account_type, account_permissions, fmt="%s", delimiter=",", newline="\n")

def get_permissions_for_group_and_accounts(admin_api_key, permission_template_input):

    env = str(permission_template_input[0])

    group_name_id_connector = get_groups_connector(admin_api_key, env)
    # print(group_name_id_connector)
    if group_name_id_connector is None:
        log_information("Groups were not properly parsed, please contact Support")
        return None

    complete_acl_list = get_complete_acl_list(admin_api_key, env)
    if complete_acl_list is None:
        log_information("Could not find any Acls from API")
        return None

    group_name = str(permission_template_input[1])

    group_id = get_group_id(group_name, group_name_id_connector)

    if group_id is None:
        log_information("Could not locate group id for group: " + group_name)
        return None

    account_type_names = get_account_names_of_template_group(admin_api_key, env, group_id)
    print(account_type_names)
    print(account_type_names[0])

    if not(account_type_names[0] is None): # Checks if there are any permissions for the AwsAccountName in Template
        AwsPermissions = get_permissions_for_group_and_account(env, admin_api_key, group_name, account_type_names[0], group_name_id_connector, complete_acl_list)
        if not(AwsPermissions is None):
            write_account_permissions("AwsPermissions.csv", AwsPermissions)
            log_information("Writing permissions for AWS Account")
        else:
            log_information("Skipping this permission because the returned permissions were None")
    else:
        log_information("No Permissions for an AWS Account in the Template")
        AwsPermissions = None

    if not(account_type_names[1] is None): # Checks if there are any permissions for the AwsMavName in Template
        AwsMavPermissions = get_permissions_for_group_and_account(env, admin_api_key, group_name, account_type_names[1], group_name_id_connector, complete_acl_list)
        if not(AwsMavPermissions is None):
            write_account_permissions("AwsMavPermissions.csv", AwsMavPermissions)
            log_information("Writing permissions for AWS MAV Account")
        else:
            log_information("Skipping this permission because the returned permissions were None")
    else:
        log_information("No Permissions for an AWS MAV Account in the Template")
        AwsMavPermissions = None

    if not(account_type_names[2] is None): # Checks if there are any permissions for the AzureAccountName in Template
        AzurePermissions = get_permissions_for_group_and_account(env, admin_api_key, group_name, account_type_names[2], group_name_id_connector, complete_acl_list)
        if not(AzurePermissions is None):
            write_account_permissions("AzurePermissions.csv", AzurePermissions)
            log_information("Writing permissions for an Azure Account")
        else:
            log_information("Skipping this permission because the returned permissions were None")
    else:
        log_information("No Permissions for an Azure Account in the Template")
        AzurePermissions = None

    if not(account_type_names[3] is None): # Checks if there are any permissions for the AzureMavName in Template
        AzureMavPermissions = get_permissions_for_group_and_account(env, admin_api_key, group_name, account_type_names[3], group_name_id_connector, complete_acl_list)
        if not(AzureMavPermissions is None):
            write_account_permissions("AzureMavPermissions.csv", AzureMavPermissions)
            log_information("Writing permissions for Azure MAV Account")
        else:
            log_information("Skipping this permission because the returned permissions were None")
    else:
        log_information("No Permissions for an Azure MAV Account in the Template")
        AzureMavPermissions = None


def cycle_permission_templates(admin_api_key, permission_template_input):
    # currently this doesn't cycle, but you can rewrite this and expand it for multiple acl sets
    for i in np.arange(0, 1): # np.shape(permission_template_input)[0]):
        output = get_permissions_for_group_and_accounts(admin_api_key, permission_template_input.iloc[0])


def main():
    file_name = "permission_template_input.csv"
    check_acl_input_file = Path(file_name)

    if check_acl_input_file.is_file():
        permission_template_input = get_permission_template_input(file_name)
    else:
        log_information("No group_permissions_input.csv found. Please write file for input")
        return

    try:
        admin_api_key = sys.argv[1]
    except IndexError:
        print("Need admin_api_key in input")
        return

    groups_list, groups_duplicate_list = get_groups(permission_template_input.iloc[0][0], admin_api_key)

    if groups_list is None:
        return

    if len(groups_duplicate_list) > 0:
        log_information("Please remove duplicate group names before proceeding.")
        return
    else:
        log_information("No duplicate groups found, please proceed.")

    cycle_permission_templates(admin_api_key, permission_template_input)


if __name__ == '__main__':
    main()