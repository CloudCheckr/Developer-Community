import numpy as np
import json
import requests
import sys

# python clear_account_families.py <admin-api-key>


def get_account_families(env, admin_api_key, payer_account_name):
    api_url = env + "api/billing.json/get_account_family_v2?access_key=" + admin_api_key + "&use_account=" + payer_account_name

    response = requests.get(api_url)
    if "AccountFamilies" in response.json():
        AccountFamilies = response.json()["AccountFamilies"]
        # print(AccountFamilies)
        return AccountFamilies
    else:
        print("Could not find any account families")
        print(response.json())
        return None


def clear_account_families(env, admin_api_key, AccountFamilies, payer_account_name, payer_account_family):
    api_url_base = env + "api/billing.json/delete_account_family"

    payer_account_family_missing = True
    for i in np.arange(0, np.shape(AccountFamilies)[0]):
        if AccountFamilies[i]["Name"] == payer_account_family:
            payer_account_family_missing = False
            break
    if payer_account_family_missing:
        print("Could not find an Account Family named " + payer_account_family)
        print("It is recommended that you create a placeholder account family that contains the payer and name it " + payer_account_family)
        return
    for i in np.arange(0, np.shape(AccountFamilies)[0]):
        api_url = api_url_base
        if not(AccountFamilies[i]["Name"] == payer_account_family):
            api_url = api_url + "?access_key=" + admin_api_key + "&use_account=" + payer_account_name + "&name=" + AccountFamilies[i]["Name"]
            response = requests.get(api_url)
            if "ModelState" in response.json() or "ErrorMessage" in response.json():
                print("Failed to delete the account family " + AccountFamilies[i]["Name"])
                print(response.json())
            else:
                print("Successfully deleted the account family " + AccountFamilies[i]["Name"])
                print(response.json())
        else:
            print("Skipping the deletion of the account family " + payer_account_family)
    print("Finished deleting account families")

def main():
    try:
        admin_api_key = str(sys.argv[1])
    except IndexError:
        print("Must admin_api_key")
        return

    env = "https://api.cloudcheckr.com/"

    payer_account_name = "Payer Master Account"  # Name of the Payer Account in CloudCheckr
    payer_account_family = "Payer Account Family"  # Name of the Account Family that contains the payer. (This account family will NOT be deleted)
    AccountFamilies = get_account_families(env, admin_api_key, payer_account_name)
    if AccountFamilies is None:
        return
    clear_account_families(env, admin_api_key, AccountFamilies, payer_account_name, payer_account_family)


if __name__ == "__main__":
    main()
