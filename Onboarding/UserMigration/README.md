# User and Group Migration

The purpose of this script is to help CloudCheckr customer's migrate their
user and groups from one region to another. (such as app to eu in order to comply
with GDPR)

CloudCheckr's DevOps team will handle the bulk of the migration and do the heavy lifting by
snapshoting the customer's RDS instance, then using the AWS Database Migration Service
to migrate the rds instance to the new region. This will migrate the customer's 
data to the new region.

This script is to help fill in some of the gaps with the migration. While the
DO migration will migate all of the AWS Accounts, the users and groups and their 
corresponding permissions will not be migrated due to the nature of how
users are stored. This script will copy the users and groups from the old region and create new users in the new region
with the copied permissions. It leverages CloudCheckr's Admin API to do this.

## Getting Started

To run the script you will have to have two separate CloudCheckr customers set up.
The first is the original customer with all the user, groups, and accounts in
the customer.

The second is the customer that the users will be copied to. This customer must
have only a single user that is an Admin. This Admin user must not be
in the original customer and is just there as a placeholder. This customer
must also have all of the same AWS Accounts and MAVs as in the original
with the *same* name. This is so the use_accout parameter can
be used to match them.

Normally DevOps will handle the migration to meet these requirements, but
you can do it as well for testing purposes. You can just add and credential
the same accounts, then make sure all the mavs and accounts have the right name.
When DevOps completes the migration, the Groups will be migrated but not have
any permissions attached to them. You will have to delete out the groups
by for example running reset_group.py. This is because there can be no
duplicate group names.

If you are migrating from one environment to the same environment (such as qa to qa),
this can be handled by creating users with the format alec@cloudcheckr.com to alec+migration@cloudcheckr.com. One limitation of this is that no emails can have 
the "+trick@cloudcheckr.com" in them. Instead, they must have the standard format.

### Customer Communication

The customer should be told in advance approximately whate time the new users
will be created, so that they are prepared for when the user activation emails
start coming in.

PartnerSysAdmin users will NOT be migrated with this script because 
the Admin API can not be used to create PartnerSysAdmins. This is on-purpose
because each PartnerSysAdmin should be carefully created and activated
due to their heightened security permissions within CloudCheckr.

### Prerequisites

What things you need to install the software and how to install them

```
python 3
pip
requests
numpy
```

### Installing

A step by step series of examples that tell you have to get a development env running.
Download migrate_users_and_groups.py, Group.py, and reset_group.py
Then install the required packages.

```
pip install requests
```

And then

```
pip install numpy
```


## Running the script

To run this python code you need the original environment such as api.
Then the original Admin API Key.
Then the new environment such as eu.
Then the new Admin API Key.

The available regions currently are api, au, eu, gov, and qa.
Currently app is not available because api calls should not
be run against app.cloudcheckr. (cough you know who your are)


For Example (invalid api keys in example)


```
python migrate_users_and_groups.py <original-region> <original-region-cloudcheckr-api-key> <new-region> <new-region-cloudcheckr-api-key>

python migrate_users_and_groups.py eu <original-region-cloudcheckr-api-key> au <new-region-cloudcheckr-api-key>
```

If you need to reset the users and groups in the new region for testing purposes,
you can run reset_users_and_groups.py. This will delete all the users and groups
in the new region and then create the placeholder admin user.

```
python reset_users_and_groups.py qa <cloudcheckr-admin-api-key>
```

### What Each file does.

migrate_users_and_groups.py ----------- is the main file that is used to migrate users and groups

Group.py ------------------------------ is a python class file used to create the group object that is used to help keep track of users in groups

reset_users_and_groups.py ------------- is used to reset users and groups in the new region if something goes wrong. Can be used for testing purposes as well.

## Deployment

It is recommended to run this on a unix based system with enough compute power
to run large and numerous api calls. Each post api call made will be logged 
for tracking purposes. 

script output3.txt can be used to store the output and view it live.

screen -r session3 can be used to run a screen while doing other things
on the console.

## Built With

* python
* numpy
* requests

## Author

* **Alec Rajeev** - *CloudCheckr Support - Tier 2*


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
