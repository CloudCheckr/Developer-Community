# Use CloudCheckr's API to Create Groups

The purpose of this script is to create groups with the CloudCheckr API.

---

## Steps to Setup Input File

1. Navigate to the CreateGroups folder.
2. In the first column write the environment such as https://api.cloudcheckr.com
3. In the second column unique name of a group that you wish to create.
4. Repeat the above for as many groups as you wish to create.

---

## Steps to Run Create Groups Program

1. Run the python program create_groups.py.
2. You must put the admin api key as a command line input. An example is below.
3. python create_groups.py 0000000000000000000000000000000000000000000000000000000000000000
4. If this runs as expected, it will ouput a groups created csv file with all the groups successfully created.

---

## How this program works.

This program will read the names of groups from the group input template csv file using pandas [read_csv](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html). These group names must be unique because of this. It will use a get request with [get_groups_v2](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_groups_v2) to check for duplicate group names and warn if there are any.

It will then loop through all of the group names and create groups with the [create_group](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#create_group) post request.

---

## CloudCheckr Group Ids

Every group will have a unique group id. This will be a UUID number.

---

## Contact

Alec Rajeev - Technical Support Engineer - Tier II
alec.rajeev@cloudcheckr.com