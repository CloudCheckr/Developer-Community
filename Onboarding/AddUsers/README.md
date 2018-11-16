# Use CloudCheckr's API to Add Users

The purpose of this script is to add users to CloudCheckr with the CloudCheckr Api.

---

## Steps to Setup Input File

1. Navigate to the AddUsers folder.
2. In the first column write the environment such as https://api.cloudcheckr.com
3. In the second column unique email that you want to add.
4. In the third column add the role that you want that user to have. The available options are Administrator, User, BasicPlusUser, BasicUser, ReadonlyUser.
4. Repeat the above for as many users that you want to create.

---

## Steps to Run Add Users program

1. Run the python program add_users.py.
2. You must put the admin api key as a command line input. An example is below.
3. python add_users.py 0000000000000000000000000000000000000000000000000000000000000000
4. If this runs as expected, it will ouput a csv file called UsersCreated with all of the users created.

---

## How this program works.

This program will read the user emails from the user input template csv file using pandas [read_csv](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html). These user names must be unique. The list of current users will be downloaded with [get_users](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_users) to get a list of current users.

It will then loop through all of the user names and add the user with the [add_user](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#add_user) post request.

---

## CloudCheckr User Id

Every user will have a unique user id. This will be a UUID number.

---

## Contact

Alec Rajeev - Technical Support Engineer - Tier II
alec.rajeev@cloudcheckr.com