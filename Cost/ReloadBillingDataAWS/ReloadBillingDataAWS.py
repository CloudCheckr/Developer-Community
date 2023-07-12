import json
import requests
import configparser


def main():
    config = configparser.RawConfigParser()
    config.read('config.txt')

    api_key = config.get('config', 'APIKey')
    api_secret = config.get('config', 'APISecret')
    customer_number = config.get('config', 'customerNumber')
    month_to_reload = config.get('config', 'monthToReload')

    print("Getting token")
    bearer_token = get_access_token("https://auth-us.cloudcheckr.com/auth/connect/token", api_key, api_secret)

    get_all_payer_accounts(customer_number, bearer_token, month_to_reload)


def get_all_payer_accounts(customer_number, bearer_token, month_to_reload):
    results = []
    print("Getting all accounts")

    url = f"https://api-us.cloudcheckr.com/customer/v1/customers/{customer_number}/accounts?accountTypes=General"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + bearer_token
    }
    response = requests.get(url, headers=headers)

    account_json = response.json()
    results.extend(account_json['items'])
    print("Results:", results)

    next_key = account_json.get('pagination', {}).get('nextKey')
    while next_key:
        print("Running while loop, nextKey detected")
        url = f"https://api-us.cloudcheckr.com/customer/v1/customers/{customer_number}/accounts?accountTypes=General&$paginationKey={next_key}"
        response_next = requests.get(url, headers=headers)
        response_json = response_next.json()
        next_key = response_json.get('pagination', {}).get('nextKey')
        if next_key:
            print("nextKey:", next_key)
        results.extend(response_json['items'])

    for item in results:
        print("Item:", item)
        if item.get("provider") == "AWS" and item.get("providerPaymentType") == 'Payer':
            print("This item is an AWS Payer:", item)
            legacy_id = item.get('legacyAccountId')
            unlock_month(legacy_id, month_to_reload, bearer_token)
            reprocess_month(legacy_id, month_to_reload, bearer_token)


def get_access_token(url, client_id, client_secret):
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    return response.json().get("access_token")


def unlock_month(legacy_id, month_to_reload, bearer_token):
    url = f"https://api.cloudcheckr.com/api/billing.json/aws_billing_report_unlock_month?access_key=bearer {bearer_token}&use_cc_account_id={legacy_id}"
    payload = json.dumps({
        "billing_month": month_to_reload,
        "lock_month": "false",
        "change_reseller_files": "true"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.text)


def reprocess_month(legacy_id, month_to_reload, bearer_token):
    url = f"https://api.cloudcheckr.com/api/billing.json/aws_billing_report_reprocess_month?access_key=bearer {bearer_token}&use_cc_account_id={legacy_id}"
    payload = json.dumps({
        "billing_month": month_to_reload,
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.text)


if __name__ == "__main__":
    main()
