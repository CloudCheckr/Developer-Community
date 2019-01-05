# Find Unmapped Accounts

Searches CloudCheckr account for any accounts which are not mapped to an account family. If it finds any, it notifies an SNS topic. The script runs during business hours by default, but this behavior can be modified by cron expression.

## Prerequisites

1. At least one AWS payer account configured as a CloudCheckr project
2. A CloudCheckr [admin API key](https://success.cloudcheckr.com/article/gbnfxmoyo6-)
3. A Systems Manager parameter named `html_encoded_semicolon_separated_master_payers` with the value(s) of the project names for AWS payer accounts in CloudCheckr, [html encoded](https://codebeautify.org/html-encode-string) and delimited by `;`

## Launch Instructions

1. Create a deployment package for the Lambda function
  * Clone to your local desktop
  * [Install NodeJS](https://nodejs.org/en/download/) if not already on your machine
  * In the the cloned directory, run `npm install` (with no options). This will create a directory called node_modules and will install dependencies based on package.json
  * Zip the node_modules folder and the validate_cc_acct_fams.js file together
2. Upload the zip to S3
3. Create a CloudFormation stack from [ValidateAccountFamilies_CF.json](ValidateAccountFamilies_CF.json) with the appropriate parameters
  * If you already have an SNS topic created, input the name and choose `false` for `CreateSnsTopic`. In this case the `PrimaryNotificationEmail` won't matter, so you can leave it blank
  * If you would like CloudFormation to create an SNS topic for you, input a name (must be unique within your account), and choose `CreateSnsTopic` `true`. Optonally enter a `PrimaryNotificationEmail`
4. You're ready to go! Confirm the SNS subscription if applicable and the CloudWatch rule + AWS Lambda will do the rest!
