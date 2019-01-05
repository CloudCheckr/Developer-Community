# Find Unmapped Accounts

Searches CloudCheckr account for any accounts which are not mapped to an account family. If it finds any, it notifies an email address via SES. SES was chosen over SNS for its ability to render HTML messages.

The script runs during business hours by default, but this behavior can be modified by cron expression.

## Prerequisites

1. At least one AWS payer account configured as a CloudCheckr project
2. A CloudCheckr [admin API key](https://success.cloudcheckr.com/article/gbnfxmoyo6-)
  * Encrypt this key as a secure string named `cc_admin_access_key` in Systems Manager parameter store and note the KMS key used for the encryption
3. A Systems Manager parameter (normal string) named `html_encoded_semicolon_separated_master_payers` with the value(s) of the project names for AWS payer accounts in CloudCheckr, [html encoded](https://codebeautify.org/html-encode-string) and delimited by `;`
4. A verified email address in SES for the `From` field, and either a verified email or [production mode](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html) active in the account

## Launch Instructions

1. Create a deployment package for the Lambda function
  * Clone to your local desktop
  * [Install NodeJS](https://nodejs.org/en/download/) if not already on your machine
  * In the the cloned directory, run `npm install` (with no options). This will create a directory called node_modules and will install dependencies based on package.json
  * Zip the node_modules folder and the validate_cc_acct_fams.js file together
2. Upload the zip to S3
3. Create a CloudFormation stack from [FindUnmappedAccounts.json](FindUnmappedAccounts.json) with the appropriate parameters
