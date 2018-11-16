# Use CloudCheckr's API to Download Example Acls

The purpose of this script is to download example Acls that will be used to create groups in the future.

---

## Steps to Setup Group Permissions Template


1. Create a group that will act as a permission template through the user-interface. Name this group Permission Template.
2. Add example permissions for each of the four account types that you with to have example permissions for. (Aws Account, Aws MAV, Azure Account, and Azure MAV). Only add one account of each type. Using multiple accounts of the same type will result in the first account being used and the later ones being skipped for example permissions.
3. Create a test user through the user-interface.
4. Assign this test user to this group Permission Template.
5. Log in as this user and verify that the permissions correspond to what you expect. Log back in as an Admin and make any adjustements that you need.
6. Once you have verified that the permissions are what you want proceed on to the next step.


---

## Steps to Download Example Acls.

1. Navigate to the GetAcls folder.
2. Delete any example permission csv files that were previously created such as AwsMavPermissions.csv. These are released for reference as an example, but should not be used unless you are just testing things.
3. Open up the permission_template_input.csv file. This will be a csv file that will be used for example input.
4. In the fist column put the environment, such as https://api.cloudcheckr.com.
5. In the second column put the name of the group that was created above. We recommend calling that group Permission Template. This file should only have one line besides the headers.
6. Run the python program get_access_control_list_per_group.py.
7. You must put the admin api key as a command line input. An example is below.
8. python get_access_control_list_per_group.py 0000000000000000000000000000000000000000000000000000000000000000
9. If this runs as expected, it will ouput permission files such as AwsPermissions.csv.
10. Copy this permissions file to the folder AddGroupPermissions. Overwrite and delete the old group permissions files.


---

## How this program works.

This program will read the name of group permission template from the input csv file using pandas [read_csv](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html). This group name must be unique because of this. The group id will be pulled with a post request using [get_groups_v2](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_groups_v2) and the group name as an input.

Using the group id, it will pull the CloudCheckr name for each of the four account types using [get_accounts_by_group](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_accounts_by_group). This will return the four account names for each account type in the group. If there are multiple account types in the group, only the first one returned will be used.

While keeping track of the account type, the group id and CloudCheckr account name will be used to find the group acls for the corresponding account type from the template. A post request with [get_access_control_list_per_group](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_access_control_list_per_group) will be used. This will pull the acls from the template.

For additional transparency to the end-user, the [get_access_control_list](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_access_control_list) will be called once to get all of the access control lists in CloudCheckr and put in a numpy array. Then using numpy's [where](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.where.html) function, the previously downloaded access control lists will be matched to a human readable permission name and section.

Then for each account type, a csv file will be generated called AwsPermissions.csv, AwsMavPermissions.csv etc. These csv files should be copied to the AddGroupPermissions folder for future use.

---

## CloudCheckr Group ACLs Info

Every group permission is defined by a particular ACL (access control list). This permission will be unique to the kind of account it is. There are four kinds of accounts Aws Accounts, Aws MAVs, Azure Accounts, and Azure MAVs.

The access control list is a long string such as 536f7e9a-c15f-4952-a289-e870f3a09930[CC_Delimiter]07ac5ec8-c453-494a-b7ed-469e3090b2b5. This string will correspond to the permission Generic,See List Costs.

We recommend setting up a template group through the UI and logging in as a test user through that group to see if the permissions align with what you expect. Then downloading the ACLs from this template group to expand to other groups. This way you can decrease how much you directly interact with these ACLs.

---

## Contact

Alec Rajeev - Technical Support Engineer - Tier II
alec.rajeev@cloudcheckr.com