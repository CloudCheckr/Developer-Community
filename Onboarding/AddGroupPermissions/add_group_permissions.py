import requests
import json
import pandas as pd
import numpy as np
import sys
import logging
from pathlib import Path
logging.basicConfig(filename='logging_for_adding_group_permissions.log',level=logging.INFO)

"""
This python script is used to add group permissions based on the group_permissions_input file.
python3 add_group_permissions.py 0000000000000000000000000000000000000000000000000000000000000000
"""

def log_information(log_string):
    logging.info(log_string)
    print(log_string)


def get_group_permissions_template_input(file_name):

    group_permissions_template_input = pd.read_csv(file_name)

    return group_permissions_template_input


def get_group_permissions(AccountPermissions_file_name):

    account_permissions = pd.read_csv(AccountPermissions_file_name)

    group_permissions = []

    for i in np.arange(0, np.shape(account_permissions)[0]):
        group_permissions.append(account_permissions.iloc[i][0])

    # print(group_permissions)
    return group_permissions

def get_project_id(account_name, account_name_id_connector):
    """
    Looks through all of the account names in the account_name_id_connector numpy array.
    Then returns the project id for that account name
    """
    for i in np.arange(0, np.shape(account_name_id_connector)[0]):
        if str(account_name_id_connector[i][0]) == str(account_name):
            return account_name_id_connector[i][1]
    return None

def get_account_type(admin_api_key, env, project_id):

    if check_invalid_env(env):
        return None

    api_url = env + "/api/account.json/get_account?access_key=" + str(admin_api_key) + "&account_id=" + str(project_id)

    r7 = requests.get(api_url)

    # TODO: expand this to work for Google. (not released yet)
    if "Provider" in r7.json():
        if "Type" in r7.json():
            provider = r7.json()["Provider"]
            account_type = r7.json()["Type"]
            if provider == "Amazon Web Services":
                if account_type == "General":
                    return "AwsPermissions"
                else:
                    if account_type == "MultiView":
                        return "AwsMavPermissions"
                    else:
                        log_information("Could not match account type and provider for project_id: " + str(project_id))
                        log_information(r7.json())
                        return None
            else:
                if provider == "Microsoft Azure":
                    if account_type == "General":
                        return "AzurePermissions"
                    else:
                        if account_type == "MultiView":
                            return "AzureMavPermissions"
                        else:
                            log_information("Could not match account type and provider for project_id: " + str(project_id))
                            log_information(r7.json())
                            return None
                else:
                    log_information("Could not match account type and provider for project_id: " + str(project_id))
                    log_information(r7.json())
                    return None
        else:
            log_information("Could not get account type for project_id: " + str(project_id))
            log_information(r7.json())
            return None
    else:
        log_information("Could not get provider for project_id: " + str(project_id))
        log_information(r7.json())
        return None


def add_group_permissions(admin_api_key, group_permissions_input_row, AccountPermissions, group_id, account_type):
    env = group_permissions_input_row[0]

    if check_invalid_env(env):
        return None
    
    api_url = env + "/api/account.json/add_access_control_lists_per_account_per_group"

    # print(AccountPermissions)

    add_acl_info = json.dumps({"group_id": group_id, "use_account": group_permissions_input_row[2], "acls": AccountPermissions})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = add_acl_info)

    if "Code" in r7.json():
        log_information("Added the acls for AccountType: " + str(account_type) + " for group: " + group_permissions_input_row[1] + " (group_id: " + str(group_id) + ") for account: " + group_permissions_input_row[2])
        log_information(r7.json())
        log_information("")
    else:
        log_information("Failed to add the acls for group: " + group_permissions_input_row[1] + " (group_id: " + str(group_id) + ") for account: " + group_permissions_input_row[2])
        log_information(r7.json())


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


def get_accounts_connector(admin_api_key, env):
    """
    Gets the list of all accounts. Generates a list of account names to project id
    """

    if check_invalid_env(env):
        return None

    api_url = env + "/api/account.json/get_accounts_v4?access_key=" + str(admin_api_key)

    r7 = requests.get(api_url)

    if "accounts_and_users" in r7.json():
        accounts_and_users = r7.json()["accounts_and_users"]
        account_name_id_connector = np.zeros((len(accounts_and_users),2), dtype="U400")
        if len(accounts_and_users) > 0:
            for i in np.arange(0, np.shape(accounts_and_users)[0]):
                if "account_name" in accounts_and_users[i] and "cc_account_id" in accounts_and_users[i]:
                    account_name_id_connector[i][0] = accounts_and_users[i]["account_name"]
                    account_name_id_connector[i][1] = accounts_and_users[i]["cc_account_id"]
                else:
                    log_information("Could not find an account_name or cc_account_id for this account")
                    log_information(str(accounts_and_users[i]))
            return account_name_id_connector
        else:
            log_information("There are no accounts in this partner")
            log_information(r7.json())
            return None
    else:
        log_information("Could not find any accounts in this partner")
        log_information(r7.json())
        return None



def cycle_add_group_permissions(admin_api_key, group_permissions_template_input, Permissions):
    """
    Finds the group id from the group name. Then adds the permissions to that group and account based on the input file.
    """

    group_name_id_connector = get_groups_connector(admin_api_key, group_permissions_template_input.iloc[0][0])
    # print(group_name_id_connector)
    if group_name_id_connector is None:
        log_information("Groups were not properly parsed, please contact Support")
        return None

    account_name_id_connector = get_accounts_connector(admin_api_key, group_permissions_template_input.iloc[0][0])

    if account_name_id_connector is None:
        return None

    # TODO: use python objects and types to make this a proper type
    AccountTypes = ["AwsPermissions", "AwsMavPermissions", "AzurePermissions", "AzureMavPermissions"]

    for i in np.arange(0, np.shape(group_permissions_template_input)[0]):
        project_id = get_project_id(group_permissions_template_input.iloc[i][2], account_name_id_connector)

        if not(project_id is None):
            account_type = get_account_type(admin_api_key, group_permissions_template_input.iloc[i][0], project_id)

            if not(account_type is None):
                if account_type in AccountTypes:
                    account_type_index = AccountTypes.index(account_type)
                    if Permissions[account_type_index] is None:
                        log_information("AccountType: " + str(account_type) + " has no permissions csv file, so skipping for group " + group_permissions_template_input.iloc[i][1] + " and account " + group_permissions_template_input.iloc[i][2])
                    else:
                        group_id = get_group_id(group_permissions_template_input.iloc[i][1], group_name_id_connector)
                        if not(group_id is None):
                            add_group_permissions(admin_api_key, group_permissions_template_input.iloc[i], Permissions[account_type_index], group_id, account_type)
                        else:
                            log_information("Could not find a group id for the group with name: " + str(group_permissions_template_input.iloc[i][1]) + " skipping row " + str(i + 2))
                else:
                    log_information("Could not find a matching account type for " + str(account_type) + " skipping row " + str(i + 2))
            else:
                log_information("Could not get the account type for the account name: " + str(group_permissions_template_input.iloc[i][2]) + " for the project_id: " + str(project_id) + " skipping row " + str(i + 2))
        else:
            log_information("Could not find a project_id for the account " + str(group_permissions_template_input.iloc[i][2]) + " skipping row " + str(i + 2))
        log_information("")


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
    file_name = "group_permissions_input.csv"

    check_group_permissions_input_file = Path(file_name)

    if check_group_permissions_input_file.is_file():
        group_permissions_template_input = get_group_permissions_template_input(file_name)
    else:
        log_information("No group_permissions_input.csv found. Please write file for input")
        return

    AwsPermissions_file_name = "AwsPermissions.csv"
    check_aws_permissions = Path(AwsPermissions_file_name)
    AwsPermissions = None
    if check_aws_permissions.is_file():
        AwsPermissions = get_group_permissions(AwsPermissions_file_name)
    else:
        log_information("No Aws Permissions found")

    AwsMavPermissions_file_name = "AwsMavPermissions.csv"
    check_aws_mav_permissions = Path(AwsMavPermissions_file_name)
    AwsMavPermissions = None
    if check_aws_mav_permissions.is_file():
        AwsMavPermissions = get_group_permissions(AwsMavPermissions_file_name)
    else:
        log_information("No Aws Mav Permissions found")

    AzurePermissions_file_name = "AzurePermissions.csv"
    check_azure_permissions = Path(AzurePermissions_file_name)
    AzurePermissions = None
    if check_azure_permissions.is_file():
        AzurePermissions = get_group_permissions(AzurePermissions_file_name)
    else:
        log_information("No Azure Account Permissions found")


    AzureMavPermissions_file_name = "AzureMavPermissions.csv"
    check_azure_mav_permissions = Path(AzureMavPermissions_file_name)
    AzureMavPermissions = None
    if check_azure_mav_permissions.is_file():
        AzureMavPermissions = get_group_permissions(AzureMavPermissions_file_name)
    else:
        log_information("No Azure Mav Account Permissions found")


    try:
        admin_api_key = sys.argv[1]
    except IndexError:
        print("Need admin_api_key in input")
        return

    groups_list, groups_duplicate_list = get_groups(group_permissions_template_input.iloc[0][0], admin_api_key)

    if groups_list is None:
        return

    if len(groups_duplicate_list) > 0:
        log_information("Please remove duplicate group names before proceeding.")
        return
    else:
        log_information("No duplicate groups found, please proceed.")

    cycle_add_group_permissions(admin_api_key, group_permissions_template_input, [AwsPermissions, AwsMavPermissions, AzurePermissions, AzureMavPermissions])


if __name__ == '__main__':
    main()
