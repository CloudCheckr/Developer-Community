import requests
import json
import sys
from datetime import datetime
import logging
logging.basicConfig(filename="logging_for_quickbooks_invoices.log",
                    level=logging.INFO)

"""
Python script used to create invoices in QuickBooks using CloudCheckr API
python quickbooks_invoices.py admin_api_key project_id realm_id access_token customer_name
(example) python3 quickbooks_invoices.py XX XX XX XX XX
"""


def log_information(log_string):
    logging.info(log_string)
    print(log_string)


def get_date():
    """
    Uses current date to get previous month information
    """

    date = datetime.today().strftime('%Y-%m')
    current_year = int(date.split('-')[0])
    current_month = int(date.split('-')[1])
    if current_month == 1:
        month = 12
        year = current_year - 1
    else:
        month = current_month - 1
        year = current_year
    end_date = 31
    months_30 = [4, 6, 9, 11]
    if month in months_30:
        end_date = 30
    if month == 2:
        if year % 4 == 0 and year % 100 != 0:
            end_date = 29
        elif year % 4 == 0 and year % 400 == 0:
            end_date = 29
        else:
            end_date = 28

    return str(year) + "-" + str(month), "-" + str(end_date)


def get_customer_id(access_token, env, realm_id, name):
    """
    Uses access token to get Customer data for Invoice API
    """

    half_url = f"{env}/v3/company/{realm_id}/query"
    api_parameters = {
        "query": f"select * from Customer where DisplayName='{name}'",
        "minorversion": "38"}
    api_headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {access_token}"}
    resp = requests.get(half_url, params=api_parameters, headers=api_headers)

    if "QueryResponse" in resp.json():
        id = resp.json()["QueryResponse"]["Customer"][0]["Id"]
        log_information(f"Obtained QuickBooks Customer data: {name}")
    else:
        log_information(f"Failed to obtain QuickBooks Customer data: {name}")
        return

    return id


def get_items(access_token, env, realm_id):
    """
    Uses access token to get Item data for Invoice API
    """

    half_url = f"{env}/v3/company/{realm_id}/query"
    api_parameters = {"query": "select * from Item", "minorversion": "38"}
    api_headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {access_token}"}
    resp = requests.get(half_url, params=api_parameters, headers=api_headers)

    items = {}

    if "QueryResponse" in resp.json():
        for item in resp.json()["QueryResponse"]["Item"]:
            items[item["Name"]] = item["Id"]
        log_information("Obtained QuickBooks Item data")
    else:
        log_information("Failed to obtain QuickBooks Item data")
        return

    return items


def get_saved_filter_results(admin_api_key, env, project_id, name, start, end,
                             items):
    """
    Uses admin API key to get Saved Filter data for invoice API
    """

    half_url = f"{env}/api/billing.json/get_detailed_billing_with_grouping_v2"
    api_parameters = {"use_cc_account_id": project_id,
                      "saved_filter_name": name, "start": f"{start}-01",
                      "end": start + end}
    api_headers = {"access_key": admin_api_key}
    resp = requests.get(half_url, params=api_parameters, headers=api_headers)

    lines = []
    missing_services = []

    if "Total" in resp.json():
        for service in resp.json()["CostsByGroup"]:
            if service["GroupValue"] not in items:
                missing_services.append(service["GroupValue"])
                continue
            for item in service["NextLevel"]:
                line = {}
                line["Amount"] = item["Cost"]
                line["Description"] = item["GroupValue"]
                line["DetailType"] = "SalesItemLineDetail"
                line["SalesItemLineDetail"] = {
                    "Qty": item["UsageQuantity"],
                    "UnitPrice": float(item["Cost"])/float(item["UsageQuantity"]),
                    "ItemRef": {
                        "value": items[service["GroupValue"]]
                    }
                }
                lines.append(line)
        log_information(f"Obtained Saved Filter data: {name}")
    else:
        log_information(f"Failed to obtain Saved Filter data: {name}")
        return

    return lines, missing_services


def create_item(access_token, env, realm_id, name, account):
    """
    Uses access token to create Item in QuickBooks
    """

    half_url = f"{env}/v3/company/{realm_id}/item?minorversion=38"
    api_parameters = {"Name": name, "Type": "Service",
                      "IncomeAccountRef": account}
    api_headers = {"Content-type": "application/json",
                   "Authorization": f"Bearer {access_token}",
                   "Accept": "application/json"}
    resp = requests.post(half_url, data=json.dumps(api_parameters),
                         headers=api_headers)

    if "Item" in resp.json():
        id = resp.json()["Item"]["Id"]
        log_information(f"Created Item: {name}")
        return id
    else:
        log_information(f"Falied to create Item: {name}")
        return


def create_invoice(access_token, env, realm_id, line, customer):
    """
    Uses access token to create Invoice in QuickBooks
    """

    half_url = f"{env}/v3/company/{realm_id}/invoice?minorversion=38"
    api_parameters = {"Line": line, "CustomerRef": customer}
    api_headers = {"Content-type": "application/json",
                   "Authorization": f"Bearer {access_token}",
                   "Accept": "application/json"}
    resp = requests.post(half_url, data=json.dumps(api_parameters),
                         headers=api_headers)

    if "Invoice" in resp.json():
        log_information(f"Created invoice")
        return
    else:
        log_information(f"Falied to create invoice")
        return


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


def validate_qbo_env(env):
    """
    Validates QBO enviroment. By default, it checks for sandbox and production.
    If you are using a standalone environment, then you must
    add it to the Environments list
    """

    Enviroments = ["https://quickbooks.api.intuit.com",
                   "https://sandbox-quickbooks.api.intuit.com"]

    if env not in Enviroments:
        log_information(f"""The QBO environment {env} is not valid. If this is a
                        standalone environment, please add the url to the
                        validate_qbo_env function.""")
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

    try:
        realm_id = str(sys.argv[3])
    except IndexError:
        log_information("Must include realm id")
        return

    try:
        access_token = str(sys.argv[4])
    except IndexError:
        log_information("Must include access token")
        return

    try:
        customer_name = str(sys.argv[5])
    except IndexError:
        log_information("Must include customer name")
        return

    env = "https://api.cloudcheckr.com"
    validate_env(env)

    qbo_env = "https://sandbox-quickbooks.api.intuit.com"
    validate_qbo_env(qbo_env)

    start, end = get_date()

    items = get_items(access_token, qbo_env, realm_id)

    line, missing_services = get_saved_filter_results(admin_api_key, env, project_id, customer_name, start, end, items)

    account = {
        "value": "82"
    }

    if missing_services:
        for service in missing_services:
            id = create_item(access_token, qbo_env, realm_id, service, account)
            items[service] = id
        line, missing_services = get_saved_filter_results(admin_api_key, env, project_id, customer_name, start, end, items)

    customer_id = get_customer_id(access_token, qbo_env, realm_id, customer_name)

    customer_id = {
        "value": customer_id
    }

    create_invoice(access_token, qbo_env, realm_id, line, customer_id)


if __name__ == '__main__':
    main()
