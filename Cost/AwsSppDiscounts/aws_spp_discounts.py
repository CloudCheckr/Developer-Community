import requests
import json
import sys
import logging
import csv
logging.basicConfig(filename="logging_for_aws_spp_discounts.log",
                    level=logging.INFO)

"""
This python script is used to configure AWS SPP discounts in CloudCheckr
python aws_spp_discounts.py admin_api_key project_id
(example) python3 aws_spp_discounts.py XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 2
"""


def log_information(log_string):
    logging.info(log_string)
    print(log_string)


def get_accounts():
    """
    Gets SPP account data from CSV file
    for edit_custom_billing_charge_monthly_percent API
    """

    sppFile = open("sample.csv")
    sppReader = csv.reader(sppFile)
    next(sppReader)
    next(sppReader)

    support = []
    net_new = []
    internal = []
    shareshift1 = []
    shareshift2 = []
    shareshift3 = []
    shareshift4 = []
    base = []
    tech = []

    for row in sppReader:
        if row[9] != "" and row[7] not in support:
            support.append(row[7])
        if row[10] != "" and row[7] not in net_new:
            net_new.append(row[7])
        if row[11] != "" and row[7] not in internal:
            internal.append(row[7])
        if row[13] == "0.01" and row[7] not in shareshift1:
            shareshift1.append(row[7])
        if row[13] == "0.02" and row[7] not in shareshift2:
            shareshift2.append(row[7])
        if row[13] == "0.03" and row[7] not in shareshift3:
            shareshift3.append(row[7])
        if row[13] == "0.04" and row[7] not in shareshift4:
            shareshift4.append(row[7])
        if row[14] != "" and row[7] not in base:
            base.append(row[7])
        if row[15] != "" and row[7] not in tech:
            tech.append(row[7])

    sppFile.close()

    log_information("Obtained SPP account data")

    if not support:
        log_information("Support Discount is empty. Please remove custom billing charge.")
    if not net_new:
        log_information("Net New Discount is empty. Please remove custom billing charge.")
    if not internal:
        log_information("Internal Discount is empty. Please remove custom billing charge.")
    if not shareshift1:
        log_information("Shareshift1 Discount is empty. Please remove custom billing charge.")
    if not shareshift2:
        log_information("Shareshift2 Discount is empty. Please remove custom billing charge.")
    if not shareshift3:
        log_information("Shareshift3 Discount is empty. Please remove custom billing charge.")
    if not shareshift4:
        log_information("Shareshift4 Discount is empty. Please remove custom billing charge.")
    if not base:
        log_information("Base Discount is empty. Please remove custom billing charge.")
    if not tech:
        log_information("Tech Discount is empty. Please remove custom billing charge.")

    return support, net_new, internal, shareshift1, shareshift2, shareshift3, shareshift4, base, tech


def get_custom_billing_charges(admin_api_key, env, project_id):
    """
    Uses admin API key to get custom billing charge data
    for edit_custom_billing_charge_monthly_percent API
    """

    half_url = f"{env}/api/billing.json/get_custom_billing_charges_v3"
    api_parameters = {"use_cc_account_id": project_id}
    resp = requests.get(half_url, params=api_parameters,
                        headers={"access_key": admin_api_key})

    if "CustomBillingCharges" in resp.json():
        custom_billing_charges = resp.json()["CustomBillingCharges"]
        for custom_billing_charge in custom_billing_charges:
            if custom_billing_charge["Description"] == "Support Discount":
                support_id = custom_billing_charge["Id"]
            if custom_billing_charge["Description"] == "Net New Discount":
                net_new_id = custom_billing_charge["Id"]
            if custom_billing_charge["Description"] == "Internal Discount":
                internal_id = custom_billing_charge["Id"]
            if custom_billing_charge["Description"] == "Shareshift1 Discount":
                shareshift1_id = custom_billing_charge["Id"]
            if custom_billing_charge["Description"] == "Shareshift2 Discount":
                shareshift2_id = custom_billing_charge["Id"]
            if custom_billing_charge["Description"] == "Shareshift3 Discount":
                shareshift3_id = custom_billing_charge["Id"]
            if custom_billing_charge["Description"] == "Shareshift4 Discount":
                shareshift4_id = custom_billing_charge["Id"]
            if custom_billing_charge["Description"] == "Base Discount":
                base_id = custom_billing_charge["Id"]
            if custom_billing_charge["Description"] == "Tech Discount":
                tech_id = custom_billing_charge["Id"]
        log_information("Obtained custom billing charge data")
    else:
        log_information("Failed to obtain custom billing charge data")
        return

    return support_id, net_new_id, internal_id, shareshift1_id, shareshift2_id, shareshift3_id, shareshift4_id, base_id, tech_id


def edit_custom_billing_charge(admin_api_key, env, project_id, charge_id,
                               accounts, name):
    """
    Uses admin API key to edit custom billing charge accounts
    """

    half_url = f"{env}/api/billing.json/edit_custom_billing_charge_monthly_percent"
    api_parameters = {"use_cc_account_id": project_id, "id": charge_id,
                      "accounts": accounts}
    resp = requests.post(half_url, data=json.dumps(api_parameters),
                         headers={"Content-type": "application/json",
                         "access_key": admin_api_key})

    if "Code" in resp.json():
        log_information(f"Modified custom billing charge: {name}")
    else:
        log_information(f"Falied to modifify custom billing charge: {name}")


def validate_env(env):
    """
    Validates enviroment. By default, it checks for api, eu, au, gov and qa.
    If you are using a standalone environment, then you must
    add it to the Environments list
    """

    Enviroments = ["https://api.cloudcheckr.com", "https://eu.cloudcheckr.com",
                   "https://au.cloudcheckr.com", "https://gov.cloudcheckr.com",
                   "https://qa.cloudcheckr.com"]

    if env not in Enviroments:
        log_information(f"""The environment {env} is not valid. If this is a
                        standalone environment, please add the url to the
                        validate_env function.""")
        return


def main():
    try:
        admin_api_key = str(sys.argv[1])
    except IndexError:
        log_information("Must include admin API key")
        return

    try:
        project_id = str(sys.argv[2])
    except IndexError:
        log_information("Must include project id")
        return

    env = "https://api.cloudcheckr.com"
    validate_env(env)

    support, net_new, internal, shareshift1, shareshift2, shareshift3, shareshift4, base, tech = get_accounts()
    support_id, net_new_id, internal_id, shareshift1_id, shareshift2_id, shareshift3_id, shareshift4_id, base_id, tech_id = get_custom_billing_charges(admin_api_key, env, project_id)
    edit_custom_billing_charge(admin_api_key, env, project_id, support_id, support, "Support Discount")
    edit_custom_billing_charge(admin_api_key, env, project_id, net_new_id, net_new, "Net New Account")
    edit_custom_billing_charge(admin_api_key, env, project_id, internal_id, internal, "Internal Discount")
    edit_custom_billing_charge(admin_api_key, env, project_id, shareshift1_id, shareshift1, "Shareshift1 Discount")
    edit_custom_billing_charge(admin_api_key, env, project_id, shareshift2_id, shareshift2, "Shareshift2 Discount")
    edit_custom_billing_charge(admin_api_key, env, project_id, shareshift3_id, shareshift3, "Shareshift3 Discount")
    edit_custom_billing_charge(admin_api_key, env, project_id, shareshift4_id, shareshift4, "Shareshift4 Discount")
    edit_custom_billing_charge(admin_api_key, env, project_id, base_id, base, "Base Discount")
    edit_custom_billing_charge(admin_api_key, env, project_id, tech_id, tech, "Tech Discount")


if __name__ == '__main__':
    main()
