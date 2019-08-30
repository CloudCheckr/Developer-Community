# QuickBooks Invoices with the CloudCheckr API

---

## Steps to Run

1. Install Python 3, https://www.python.org/downloads/
2. Install requests, logging, and datetime libraries with pip
3. Log into CloudCheckr and create an Admin API access key at Admin Functions >> Admin API Key, https://app.cloudcheckr.com/Project/GlobalApiCredentials
5. Log into QuickBooks and create an App, https://developer.intuit.com/app/developer/myapps
6. Select the App and generate an Access Token via OAuth 2.0 with an Accounting scope, https://developer.intuit.com/app/developer/playground
7. Run python quickbooks_invoices.py <cloudcheckr-admin-api-key> <payer-project-id> <quickbooks-realm-id> <quickbooks-access-token> <customer-name>

---

## How the program works

Uses [get_detailed_billing_with_grouping_v2](https://success.cloudcheckr.com/article/7sskuffbg6-api-reference-guide#list_results_from_an_advanced_grouping_saved_filter) API to get Saved Filter data for QuickBooks Invoice API.

Uses [item_query](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/item#query-an-item) & [customer_query](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/customer#query-a-customer) API to get Item and Customer data for QuickBooks Invoice API.

Uses [item](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/item#create-an-item) API to create Items for QuickBooks Invoice API.

Uses [invoice](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/invoice) API to create Invocies in QuickBooks.

The payer project ID is the CloudCheckr project ID of the AWS Payer account. Project ID information can be obtained using the [get_accounts_v4](https://success.cloudcheckr.com/article/kr5glkrmon-admin-api-reference-guide#get_accounts_v4) API. Project ID is also known as cc_account_id. 

Saved Filters can be viewed through the CloudCheckr UI at Cost >> AWS Billing >> Custom Reporting >> Advanced Grouping.

---

## Assumptions

1. The CloudCheckr environment is set at https://api.cloudcheckr.com. It can be adjusted on line 249 if required.
2. The QuickBooks environment is set at https://sandbox-quickbooks.api.intuit.com. It can be adjusted on line 252 if required.
3. The QuickBooks Account ID needs to be set. It can be adjusted on line 262.
4. The QuickBooks "DisplayName" and CloudCheckr "Saved Filter" name must match in order to successfully generate an invoice. 
5. Saved Filter used must contain at least two group-by levels. The first group-by level will map to the "Service" attribute and the second group-by level will map to the "Activity" attribute. The "Service" and "Activity" attributes will be included as part of the QuickBooks invoice. 