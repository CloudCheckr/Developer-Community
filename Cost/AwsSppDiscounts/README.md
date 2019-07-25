# AWS SPP Discounts with the CloudCheckr API

---

## Steps to Run

1. Install python 3, https://www.python.org/downloads/
2. Install requests, logging, and csv libraries with pip
3. Log into CloudCheckr and create an Admin API access key at Admin Functions >> Admin API Key, https://app.cloudcheckr.com/Project/GlobalApiCredentials
4. Run python aws_spp_discounts.py <cloudcheckr-admin-api-key> <payer-project-id>

---

## How the program works

Uses AWS provided CSV file to add accounts to corresponding Custom Billing Charge buckets.

If a Custom Billing Charge bucket is empty, it asks that the Custom Billing Charge be deleted. Custom Billing Charges must include at least one account. 

Uses [get_custom_billing_charges_v3](https://success.cloudcheckr.com/article/kr5glkrmon-admin-api-reference-guide#get_custom_billing_charges_v3) API call to get custom billing charge data for edit_custom_billing_charge_monthly_percent API call.

Uses [edit_custom_billing_charge_monthly_percent](https://success.cloudcheckr.com/article/kr5glkrmon-admin-api-reference-guide#edit_custom_billing_charge_monthly_percent) API call to add accounts to Custom Billing Charge configurations.

The payer project id is the CloudCheckr project id of the AWS Payer account.

Custom Billing Charges can be viewed through the UI at Cost >> AWS Partner Tools >> Configure >> Custom Billing Charges.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 178 if required.
2. The Custom Billing Charge names are defined at lines 102 to 118. If names do not match current Custom Billing Charge configuration, please redefine names.