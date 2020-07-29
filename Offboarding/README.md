**Offboard Accounts with Python and CloudCheckr API**

1) This python script is used to delete accounts based on the list of accounts provided in a csv file named 'accounts_list'.  Please see example datafile for formatting (example_datafile_delete_accounts.csv).
2) For the data file, please define 2 columns:
   - Column 1: the API URI for your region in CloudCheckr
       - Valid regions:
           - https://api.cloudcheckr.com
           - https://eu.cloudcheckr.com
           - https://au.cloudcheckr.com
           - https://gov.cloudcheckr.com
   - Column 2: the corresponding account name of the account you wish to be deleted (as it appears in the CloudCheckr landing page)
    Note:  The first row is for column names
3) To call this script, use the following: python3 delete_accounts.py <admin level access key>
4) Please ensure that this file is in the same folder/directory as the data file.
5) Once the script has completed, please check the log file for errors to validate that all your anticipated changes were successfully made by the API.  If you do see errors and need assistance, CloudCheckr Support may be able to provide further assistance if an Error Identity code is found in the logs.  Please provide us the log file so that we may look into the error. 
