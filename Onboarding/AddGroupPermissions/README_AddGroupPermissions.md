# Use CloudCheckr's API to Add Permissions to Groups

The purpose of this script is to use the acls that were previously downloaded and add them to groups.

---

## Steps to Setup Input File

1. Navigate to the AddGroupPermissions folder.
2. In the first column write the environment such as https://api.cloudcheckr.com
3. In the second column unique name of a group that you want to add a permission to.
4. In the third column write the name of the account in CloudCheckr that you wish to add permissions for that account to.
5. Repeat the above for as many groups and accounts that you want to add permissions to.
6. Each group and account should have its own line.
7. Make sure the that AwsPermissions.csv, AwsMavPermissions.csv etc files are the permissions that you generated in a previous step. When the program is first downloaded, the will be no files here so the program will not run. You may have to go back to the GetAcls folder and copy the csv files here.
8. The file names for the permission csv files are hard coded in this program.

---

## Steps to Add Group Permissions.

1. Run the python program add_group_permissions.py.
2. You must put the admin api key as a command line input. An example is below.
3. python add_group_permissions.py 0000000000000000000000000000000000000000000000000000000000000000
4. If this runs as expected, it will ouput the group and accounts that had permissions added to the command line and log.

---

## How this program works.

This program will read the list of group permissions for every account type from the Permission csv files using pandas [read_csv](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html). Then it will read the accounts and groups that you want to add permissions for from the groups_perimssions_input.csv file.

Then it will build a numpy array that links the group names and group ids with [get_groups_v2](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_groups_v2). Group names must be unique because of this.

It will then loop through all of the accounts that you want to add permissions for and get the account type with [get_account](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_account). Then based on the account type it will connect that to the corresponding permissions list that was imported from the csv file.

With the group id, acl list, and account name known, it will then use a post request to add permissions with [add_access_control_lists_per_account_per_group](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#add_access_control_lists_per_account_per_group)]. This action will be logged to the command line.

If an account needs permissions, but there is no corresponding permissions list for that account type it will be skipped and logged.

---

## CloudCheckr Group ACLs Info

Every group permission is defined by a particular ACL (access control list). This permission will be unique to the kind of account it is. There are four kinds of accounts Aws Accounts, Aws MAVs, Azure Accounts, and Azure MAVs.

The access control list is a long string such as 536f7e9a-c15f-4952-a289-e870f3a09930[CC_Delimiter]07ac5ec8-c453-494a-b7ed-469e3090b2b5. This string will correspond to the permission Generic,See List Costs.

We recommend setting up a template group through the UI and logging in as a test user through that group to see if the permissions align with what you expect. Then downloading the ACLs from this template group to expand to other groups. This way you can decrease how much you directly interact with these ACLs.

---

## CloudCheckr Group Ids

Every group will have a unique group id. This will be a UUID number.

---

## Contact

Alec Rajeev - Technical Support Engineer - Tier II
alec.rajeev@cloudcheckr.com