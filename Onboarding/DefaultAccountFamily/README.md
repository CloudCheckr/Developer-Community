# Default Account Family with the CloudCheckr API

---

## Steps to Run

1. Install python 3. https://www.python.org/downloads/
2. Install requests and logging libraries with pip
3. Log into CloudCheckr and create an Admin API access key at Admin Functions >> Admin API Key, https://app.cloudcheckr.com/Project/GlobalApiCredentials
4. Run python default_account_family.py <cloudcheckr-admin-api-key>

---

## How the program works

Uses [get_account_family_v2](https://success.cloudcheckr.com/article/kr5glkrmon-admin-api-reference-guide#get_account_family_v2) API call to get account data for modify_account_family API call.

Uses [modify_account_family](https://success.cloudcheckr.com/article/kr5glkrmon-admin-api-reference-guide#modify_account_family) API call to add all unmapped accounts to default account family.

The payer project id is set at line 86. 

The default account familty is set at line 87.

You can view CloudCheckr Account Families through the UI at Cost >> AWS Partner Tools >> Configure >> Account Families.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 83 if required.
