import requests
import json
import sys
import numpy as np

# python3 reset_users_and_groups.py qa 0000000000000000000000000000000000000000000000000000000000000000
# used to reset the second environment if you would like to start fresh


def get_groups(env, admin_api_key):
    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/get_groups_v2"

    r1 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})

    if ('ErrorCode' in r1.json()):
        if (r1.json()['ErrorCode'] == "NotFound"):
            print("No Groups")
            return None
    # print(r1.json())
    # print(r1.json()['Groups'])
    return r1.json()['Groups']

def delete_group(env, admin_api_key, group_id):
    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/delete_group"
    r2 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = json.dumps({"group_id": group_id}))

def delete_groups(env, admin_api_key, groups):
    if (groups is None):
        return
    for i in np.arange(0, np.size(groups)):
        delete_group(env, admin_api_key, groups[i]["Id"])
        print("Deleted Group " + groups[i]["Id"])

def get_users(env, admin_api_key):
    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/get_users_v2"   
    r1 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})
    users = r1.json()['user_permissions']

    return users

def delete_user(env, admin_api_key, user_email):
    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/remove_user"    
    
    # print(user_email)
    r2 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = json.dumps({"email": user_email}))
    # print(r2.json())
    if ('ModelState' in r2.json()):
        print(user_email + " failed to be deleted")
        print(r2.json())
    else:
        print(user_email + " was deleted")

def add_user(env, admin_api_key, env_type, email, role, group_name):
    """
    Adds a user to the new environment. Will only add to a gorup if the user is in a group.
    Will add functionality around logon rules later.
    Can't use add_users because users in the same group could have different roles.
    """

    api_url = "https://" + env + ".cloudcheckr.com/api/account.json/add_user"

    r7 = None

    # email = get_corrected_email(email, env_type)

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
                print("Created the user " + email + " in the group" + group_name)
                print(r7.json())
        else:
            print("Failed to create user " + email)
            print(r7.json())
    return email

def delete_users(env, admin_api_key, users):
    if (users is None):
        print("no users")
        return
    for i in np.arange(0, np.shape(users)[0]):
        delete_user(env, admin_api_key, users[i]["email"])

def main():
    print("Reset Groups and Users\n")
    env = sys.argv[1]
    admin_api_key = sys.argv[2]
    groups = get_groups(env, admin_api_key)
    delete_groups(env, admin_api_key, groups)
    users = get_users(env, admin_api_key)
    delete_users(env, admin_api_key, users)
    # print("\n")
    # adds a simple admin, because later when you try to add a user without an Admin, it throws an error
    add_user(env, admin_api_key, 1, "example2@example.com", "Administrator", None)

if __name__ == '__main__':
    main()