reloadbillingdataaws.py
Author: Kurt Jordan

This script is designed to recognize each payer account in your environment and reprocess the month designated in the config file.
requirements:

edit the config.txt file to include the following:

APIKey -  use the following to create the api key and secret. https://success.cloudcheckr.com/article/93urirlmng-cloudcheckr-cmx-api
APISecret - permissions needed: [CloudCheckr API Access][Full Administration]
customerNumber - can be obtained in the URL of CloudCheckr behind https://app-us.cloudcheckr.com/customers/xxxxxx
monthToReload = 2023-06-01