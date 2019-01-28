import requests
import json
import sys
import logging
logging.basicConfig(filename='logging_for_modify_users.log',level=logging.INFO)

"""
This python script is used to modify users based on a specified criteria and desired result
python3 modify_users.py 0000000000000000000000000000000000000000000000000000000000000000
"""

def log_information(log_string):
    logging.info(log_string)
    print(log_string)


def get_users_v2(admin_api_key, env):
    """
    Uses admin API key to get user data
    """
    
    half_url = f"{env}/api/account.json/get_users_v2"
    api_parameters = {}
    resp = requests.get(half_url, params=api_parameters, headers = {"access_key": admin_api_key})
    
    users = []

    if "user_permissions" in resp.json():
        user_data = resp.json()["user_permissions"]
        for user in user_data:
            if user["role"] == "PartnerSysAdmin":
                users.append(user["email"])
    else:
        log_information("Unable to obtain user data")
    
    return users


def edit_user(admin_api_key, env, user):
    """
    Uses admin API key to modify user
    """
    
    half_url = f"{env}/api/account.json/edit_user"
    api_parameters = {"email": user, "role": "Administrator"}
    resp = requests.post(half_url, data=json.dumps(api_parameters), headers = {"Content-type": "application/json", "access_key": admin_api_key})

    if "Code" in resp.json():
        log_information(f"Modified user with email: {user}")
    else:
        log_information(f"Failed to modify user with email: {user}")


def validate_env(env):
    """
    Validates environment. By default, it checks for api, eu, au, gov and qa.
    If you are using a standalone environment, then you must add it to the environments list
    """

    enviroments = ["https://api.cloudcheckr.com", "https://eu.cloudcheckr.com", "https://au.cloudcheckr.com", "https://gov.cloudcheckr.com", "https://qa.cloudcheckr.com"]

    if env not in enviroments:
        log_information(f"The environment {env} is not valid. If this is a standalone environment, please add the url to the validate_env function.")


def main():
    try:
        admin_api_key = str(sys.argv[1])
    except IndexError:
        log_information("Must include admin API key")
        return

    env = "https://api.cloudcheckr.com"
    validate_env(env)

    users = get_users_v2(admin_api_key, env)
    for user in users:
        edit_user(admin_api_key, env, user)


if __name__ == '__main__':
    main()