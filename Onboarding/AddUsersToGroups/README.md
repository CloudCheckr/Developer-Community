# Use CloudCheckr's API to Add Users To Groups

The purpose of this script is to add users to groups with the CloudCheckr Api.

---

## Steps to Setup Input File

1. Navigate to the AddUsers folder.
2. In the first column write the environment such as https://api.cloudcheckr.com
3. In the second column write the email of the user that you want to add to a group.
4. In the third column write the group name that you wish to add that user to.
4. Repeat the above for as many users that you want to add to groups.

---

## Steps to Run Add Users program

1. Run the python program add_users_to_groups.py.
2. You must put the admin api key as a command line input. An example is below.
3. python add_users_to_groups.py 0000000000000000000000000000000000000000000000000000000000000000
4. If this runs as expected, it will log all of the users that were added to groups on the command line.

---

## How this program works.

This program will read the users and groups from the add_users_to_groups input template csv file using pandas [read_csv](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html).

It will then generate a numpy array to connect group names to group id with a get request on [get_groups_v2](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_groups_v2).

It will then loop through all of the user names (emails) and ge the user id with a post request on [get_user_v2](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_user_v2) using the email as an input.

With the corresponding user id and group id, it will then add the user to the group with [add_user_to_group](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#add_user_to_group). Every user added to a group will be logged to the command line.

---

## CloudCheckr User Id

Every user will have a unique user id. This will be a UUID number.

---

## CloudCheckr Group Id

Every user will have a unique group id. This will be a UUID number.

---

## Contact

Alec Rajeev - Technical Support Engineer - Tier II
alec.rajeev@cloudcheckr.com