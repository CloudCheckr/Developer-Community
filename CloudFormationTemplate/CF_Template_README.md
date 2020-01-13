# CloudFormation Template

A cross-account role allows you to share resources across AWS accounts. Since your cross-account role works globally, you don't need IAM users to sign in and out of accounts to access these resources.

The CloudFormation template is an alternative to creating a cross-account role manually. It is a JSON file pre-configured with all the parameters and provisions you need to access your AWS resources across multiple accounts in your cloud environment. This template allows AWS to standardize permissions across your deployment automatically.

To view a detailed list of instructions, please go to https://success.cloudcheckr.com/article/3ldmqs5pzn-creating-aws-credentials-with-cloud-formation for more details.

Please note, our CloudFormation template is only intended to credential Commercial AWS Accounts.  For GovCloud accounts, IAM Access Keys will be required, more details can be found at https://success.cloudcheckr.com/article/99vns4x2ho-configure-gov-cloud-account-iam-access-keys.

## Policy Structure Notes

### Unauthorized Access

CloudCheckr will attempt to ingest data from all of the AWS core features to populate the Cost, Billing, Security, Inventory, and CloudWatch Flow Log reports. Since CloudCheckr must make calls even to those categories where you have not enabled permissions, you will see "Unauthorized Access" attempts in your CloudTrail logs. These logs are only an indication of the CloudCheckr workflow and in no way reflect an attempt on the part of CloudCheckr to collect unauthorized information from customers.

### s3:GetObject

To help you maintain a secure, least privilege configuration, CloudCheckr's Security/Compliance policy does not include any `s3:GetObject` permissions. However, you can add add the `s3:GetObject` permission to the following reports:

* S3 Encryption Details report: enables CloudCheckr scan your encrypted S3 buckets.
  * We recommend restricting this permission to only selected S3 bucket(s).

* List of VPCs report: enables CloudCheckr to ingest data from the Elastic Beanstalk applications for this report.
  * The default Security/Compliance policy will only display 0 as the number of Elastic Beanstalk applications within a VPC.

### s3:GetEncryptionConfigruation

As per the latest AWS requirements, CloudCheckr's CloudFormation template and the Inventory policy do not include the "s3:GetEncryptionConfiguration" by default.
However, without this permission, CloudCheckr cannot get the information it needs to report on the "S3 Bucket Without Default Encryption Enabled" Best Practice Check (BPC). If you decide not to add this permission to your policy, we recommend that you ignore or disable this BPC to avoid any false negatives.
