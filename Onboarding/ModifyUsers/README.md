# Modify Users with the CloudCheckr API

---

## Steps to Run

1. Install python 3. https://www.python.org/downloads/
2. Install requests and logging python libraries with pip3
3. Log into CloudCheckr and create an Admin API access key at Admin Functions >> Admin API Key, https://app.cloudcheckr.com/Project/GlobalApiCredentials
4. Run python3 modify_users.py <cloudcheckr-admin-api-key>

---

## How the program works

Uses the [get_users_v2](https://success.cloudcheckr.com/article/kr5glkrmon-admin-api-reference-guide#get_users_v2) API call to get user data from an environment.

Uses the [edit_user](https://success.cloudcheckr.com/article/kr5glkrmon-admin-api-reference-guide#edit_user) API call to modify users.

The criteria is set at line 30. 

The desired result is set at line 44.

The program is set to modify users with user role, PartnerSysAdmin, to user role, Administrator.

You can view CloudCheckr Users through the UI at Settings >> Users.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 71 if required.