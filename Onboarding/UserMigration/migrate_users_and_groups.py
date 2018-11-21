import requests
import json
import sys
import numpy as np

from Group import Group

# python3 migrate_users_and_groups.py.py qa 0000000000000000000000000000000000000000000000000000000000000000 qa 0000000000000000000000000000000000000000000000000000000000000000

def get_groups(env, admin_api_key):
    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/get_groups_v2"

    r1 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})

    if ('ErrorCode' in r1.json()):
        if (r1.json()['ErrorCode'] == "NotFound"):
            # print("No Groups")
            return None
    # print(r1.json())
    # print(r1.json()['Groups'])
    # print("Grabbed list of groups\n")
    return r1.json()['Groups']

def check_duplicate_group(env2, admin_api_key2, group_name):
    # you have to do this becaues the only way to add users to group is with add_user(s) call which requires a unique group name
    groups2 = get_groups(env2, admin_api_key2)
    if (groups2 is None): # if there are no groups yet, then this should return false because there can't be a duplicate
        return False
    else:
        list_of_groups = np.full(np.shape(groups2)[0], "group-name-heref6a-bdab-1c3b9a4f5ced")
        for j in np.arange(0, np.shape(groups2)[0]):
            list_of_groups[j] = groups2[j]['Name']

        return np.any(np.isin(list_of_groups, group_name))


def create_group(env2, admin_api_key2, group_name):
    # add a validator to make sure there are no groups with two names
    if not (check_duplicate_group(env2, admin_api_key2, group_name)):
        api_url = "https://" + env2 + ".cloudcheckr.com/api/account.json/create_group"

        r3 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key2}, data = json.dumps({"name": group_name}))
        if ("Message" in r3.json()):
            if (r3.json()["Message"] == "OK"):
                print("Created Group: " + group_name + " in " + env2 + " with id: " + r3.json()["group_id"])
                print(r3.json())
                return r3.json()["group_id"]
            else:
                print("Could not create group " + group_name)
                print(r3.json())
        else:
            print("Could not create group " + group_name)
            print(r3.json())
    else:
        print("Duplicate Group Name not Supported. Change group name " + group_name + " of original environment")

    return None



def create_groups(env1, admin_api_key1, env2, admin_api_key2, groups):
    """
    Gets the list of groups from the original environment and migrates them to the new environment
    It is limited, so a group name can not be duplicated.
    """

    # print(np.shape(groups))
    group_links = np.full((np.shape(groups)[0],3), "00000000-0000-0000-0000-000000000000")
    # print(group_links)

    for i in np.arange(0, np.shape(groups)[0]):
        group_links[i][0] = groups[i]["Id"]
        new_group_id = create_group(env2, admin_api_key2, groups[i]['Name'])
        if not (new_group_id is None):
            group_links[i][1] = new_group_id
            group_links[i][2] = groups[i]["Name"]

    # print(group_links)
    print("Finished Creating groups\n")

    return group_links

def get_accounts_in_group(env, admin_api_key, group_id):
    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/get_accounts_by_group?group_id=" + group_id

    r4 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})

    if ("ErrorCode" in r4.json()):
        print("No accounts permissionsed in this group " + group_id)
        return None
    else:
        projects = r4.json()["Projects"]
        use_account_list = np.full(np.shape(projects)[0], "00000000-0000-0000-0000-000000000000")
        for i in np.arange(0, np.size(use_account_list)):
            use_account_list[i] = projects[i]["Name"]
        return use_account_list

def get_list_of_group_acls_for_account(env, admin_api_key, group_id, account_name):
    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/get_access_control_list_per_group?group_id=" + group_id + "&use_account=" + account_name

    r5 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})

    if ("ErrorCode" in r5.json()):
        print(r5.json())
        return None
    else:
        if not ("Acls" in r5.json()):
            return None
        acls = r5.json()["Acls"]
        list_of_acls = []
        for i in np.arange(0, np.shape(acls)[0]):
            list_of_acls.append(acls[i]["Id"])
        return list_of_acls

def add_group_permissions_for_account(env1, admin_api_key1, env2, admin_api_key2, group1_id, group2_id, account_name):
    list_of_acls = get_list_of_group_acls_for_account(env1, admin_api_key1, group1_id, account_name)

    if not (list_of_acls is None):
        api_url = "https://" + env2 + ".cloudcheckr.com/api/account.json/add_access_control_lists_per_account_per_group"
        r6 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key2}, data = json.dumps({"group_id": group2_id, "use_account": account_name, "acls": list_of_acls}))
        # print(r6.json())
        if not ("ErrorCode" in r6.json()):
            if ("Id" in r6.json()):
                print("Added Group Permissions from " + group1_id + " to " + r6.json()["Id"] + " for the account " + account_name)
                print(r6.json())
            else:
                print("Could NOT add group permissions from " + group1_id + " to group2_id for the account " + account_name)
                print(r6.json())
        else:
            print("Could NOT add group permissions from " + group1_id + " to group2_id for the account " + account_name)
            print(r6.json())
    else:
        print("Could NOT add group permissions from " + group1_id + " to group2_id for the account " + account_name)
        print(r6.json())

def add_group_permissions(env1, admin_api_key1, env2, admin_api_key2, group1_id, group2_id):
    """
    For every account in a group add the associated permissions for the account
    """

    use_account_list = get_accounts_in_group(env1, admin_api_key1, group1_id)
    if not (use_account_list is None):
        for i in np.arange(0, np.size(use_account_list)):
            if not (use_account_list[i] is None):
                add_group_permissions_for_account(env1, admin_api_key1, env2, admin_api_key2, group1_id, group2_id, use_account_list[i])
    
def add_groups_permissions(env1, admin_api_key1, env2, admin_api_key2, group_links):
    """
    For every group add the permissions for all of the associated accounts
    """
    for i in np.arange(0, np.shape(group_links)[0]):
        add_group_permissions(env1, admin_api_key1, env2, admin_api_key2, group_links[i][0], group_links[i][1])

    print("Finished adding All Groups Permissions\n")

def environment_validator(env):
    """
    Checks if the passed in environment is a valid one. like qa or eu
    """
    if (env is None):
        print("environment is blank")
        return False # can't use app because when using the api, you should be using api.cloudcheckr.com
    if (env == "qa" or env == "api" or env == "eu" or env == "au"):
        return True

def environment_checkr(env1, env2):
    """
    Checks whether or not you have to add +migration to a username if the environments are the same
    returns -1 if the environments are invalid
    returns 0 if you have to the +migration
    returns 1 if it is strictly from qa to app
    """

    if (environment_validator(env1) and environment_validator(env2)):
        if (env1 != env2):
            return 1
        else:
            return 0 # must add the +migration to user
    else:
        return -1

def get_users_in_group(env, admin_api_key, group_link_row):
    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/get_users_by_group?group_id=" + group_link_row[0]

    r1 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})

    if ("ErrorCode" in r1.json()):
        print("No users in the group " + group_link_row[2])
        return None
    else:
        Users = r1.json()["Users"]
        users_list = np.full(np.shape(Users)[0], "user-name-heref6a-bdab-1c3b9a4f5ced")
        for i in np.arange(0, np.shape(Users)[0]):
            users_list[i] = Users[i]["Email"]

        if (np.size(users_list) == 0):
            return None
        return users_list

def build_group_objects(env1, admin_api_key1, group_links):
    """
    Builds a list of Group objects that will be used to more quickly check for users in groups
    """
    Groups_List = [] # initialize a python list of objects

    if not (group_links is None):
        for i in np.arange(0, np.shape(group_links)[0]):
            g1 = Group(group_links[i][0],group_links[i][1], group_links[i][2])
            g1.add_users(get_users_in_group(env1, admin_api_key1, group_links[i]))
            Groups_List.append(g1)
        return Groups_List
    else:
        return None

def build_groups(env1, admin_api_key1, env2, admin_api_key2):
    """
    Builds the groups in the new environment and copies over the permissions
    """
    groups = get_groups(env1, admin_api_key1)
    print("Grabbed Original Group List")
    if (groups is None): # this script should work even if there are no groups
        print("No Groups in original environment")
        return None
    else:
        group_links = create_groups(env1, admin_api_key1, env2, admin_api_key2, groups)
        print("Start adding group permissions")
        add_groups_permissions(env1, admin_api_key1, env2, admin_api_key2, group_links)

        Groups_List = build_group_objects(env1, admin_api_key1, group_links)

        return group_links, Groups_List

def get_users(env, admin_api_key):
    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/get_users_v2"   
    r1 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})
    
    if not ("ErrorCode" in r1.json()):
        return r1.json()["user_permissions"]
    else:
        return None

def get_group_name_of_user(Groups_List, user_email):
    if (Groups_List is None):
        return None
    if (np.size(Groups_List) is None):
        return None
    for i in np.arange(0, np.size(Groups_List)):
        if (Groups_List[i].check_user(user_email)):
            return Groups_List[i].name
    return None # user isn't in a group


def get_corrected_email(email, env_type):
    """
    If you are transfering users from qa to qa, you have to add +migration to make the users unique.
    (cheating a bit)
    """
    if (env_type):
        return email

    # I should add functionality to handle an initial email with a +qa part

    split_array = email.split("@")
    return split_array[0] + "+migration" + "@" + split_array[1]

def add_user(env, admin_api_key, env_type, email, role, group_name):
    """
    Adds a user to the new environment. Will only add to a gorup if the user is in a group.
    Will add functionality around logon rules later.
    Can't use add_users because users in the same group could have different roles.
    """

    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/add_user"

    r7 = None

    email = get_corrected_email(email, env_type)

    if (group_name is None):
        r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = json.dumps({"email": email, "user_role": role}))
    else:
        r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = json.dumps({"email": email, "user_role": role, "group": group_name}))

    if ("Message" in r7.json()):
        print("Failed to create new user " + email)
        print(r7.json())
    else:
        if ("CreationStatuses" in r7.json()):
            if (group_name is None):
                print("Created the user " + email)
                print(r7.json())
            else:
                print("Created the user " + email + " in the group " + group_name)
                print(r7.json())
        else:
            print("Failed to create user " + email)
            print(r7.json())
    return email


def add_users(env1, admin_api_key1, env2, admin_api_key2, env_type, users, Groups_List):
    """
    Adds all the users to the new account. Will add to a group if the user is currently in a group.
    """
    if (users is None):
        print("No users in the account")
        return None
    if (np.shape(users)[0] == 0):
        print("No users in the account")
        return None
    
    for i in np.arange(0, np.shape(users)[0]):
        group_name = get_group_name_of_user(Groups_List, users[i]["email"])
        add_user(env2, admin_api_key2, env_type, users[i]["email"], users[i]["role"], group_name)

    print("Finished Creating Users\n")

def add_account_permissions_for_user(env, admin_api_key, email, account_permissions):

    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/grant_account"

    # print(account_permissions["account"])
    permissions = account_permissions["permissions"]

    access_account = False
    for i in np.arange(0, np.shape(permissions)[0]):
        if (permissions[i]["is_granted"] == "yes"):
            access_account = True
            break

    # if there are no permissions for the account, then don't give it any access
    # exit this function
    if not (access_account):
        return

    r8 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = json.dumps(
        {"email": email, "use_account": account_permissions["account"],
        "replace_existing_permissions": "1",
        "cost_report": permissions[0]["is_granted"],
        "blended_cost": permissions[1]["is_granted"],
        "credits": permissions[2]["is_granted"],
        "resource_utilization_reports": permissions[3]["is_granted"],
        "trending_reports": permissions[4]["is_granted"],
        "change_monitoring": permissions[5]["is_granted"],
        "best_practices": permissions[6]["is_granted"],
        "unblended_cost": permissions[7]["is_granted"],
        "list_cost": permissions[8]["is_granted"],
        "edit_emails": permissions[9]["is_granted"],
        "automation": permissions[10]["is_granted"],
        "alert": permissions[11]["is_granted"],
        "security": permissions[12]["is_granted"],
        "inventory": permissions[13]["is_granted"],
        "savings": permissions[14]["is_granted"],
        "account_notification": permissions[15]["is_granted"],
        "partner_tools": permissions[16]["is_granted"],
        "edit_partner_tools": permissions[17]["is_granted"],
        "see_api_keys": permissions[18]["is_granted"]
        }))

    if ("ModelState" in r8.json()):
        print("Did NOT give the user " + email + " permissions to account " + account_permissions["account"])
    else:
        print("Gave user " + email + " permissions to account " + account_permissions["account"])

    return


def add_accounts_permissions_for_user(env, admin_api_key, email, account_permissions):
    if (account_permissions is None):
        return

    if (np.shape(account_permissions)[0] == 0):
        return

    for i in np.arange(0, np.shape(account_permissions)[0]):
        add_account_permissions_for_user(env, admin_api_key, email, account_permissions[i])

def add_user_permissions(env2, admin_api_key2, env_type, users):
    """
    Grants Account Level permissions to Users and BasicUsers
    """
    if (users is None):
        print("No Users")
        return None
    if (np.shape(users)[0] == 0):
        print("No Users")
        return None

    print("Start adding user account level permissions")
    for i in np.arange(0, np.shape(users)[0]):
        email = get_corrected_email(users[i]["email"], env_type)
        account_permissions = users[i]["account_permissions"]
        if not (users[i]["role"] == "Administrator"): # eventually add PartnerSysAdmin
            add_accounts_permissions_for_user(env2, admin_api_key2, email, account_permissions)
    print("\nFinished adding user account level permissions")

def build_users(env1, admin_api_key1, env2, admin_api_key2, env_type, group_links, Groups_List):
    users = get_users(env1, admin_api_key1)
    add_users(env1, admin_api_key1, env2, admin_api_key2, env_type, users, Groups_List)
    add_user_permissions(env2, admin_api_key2, env_type, users)

def main():
    env1 = sys.argv[1]
    admin_api_key1 = sys.argv[2]
    env2 = sys.argv[3]
    admin_api_key2 = sys.argv[4]

    print("Migrate Users and Groups from " + env1 + " to " + env2)

    env_type = environment_checkr(env1, env2)
    if (env_type < 0):
        print("Environments are invald " + env1 + " " + env2)
        return

    if (env_type):
        print("Migration is between different regions\n")
    else:
        print("Migation is in the same region\n")

    group_links, Groups_List = build_groups(env1, admin_api_key1, env2, admin_api_key2)

    build_users(env1, admin_api_key1, env2, admin_api_key2, env_type, group_links, Groups_List)

    # api call doesn't support partnersys admins
    print("Finished running user-migration script")



if __name__ == '__main__':
    main()