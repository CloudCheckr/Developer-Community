# AWS Control Tower Integration


## What is this?

This is the folder that contains the CloudCheckr CMx AWS Control Tower Integration. AWS Control Tower is a Service that allows customers to more easily govern and secure a multi-account AWS environment. This CloudCheckr CMx AWS Control Tower integration allows customers to more easily add new AWS accounts to CloudCheckr.

## Why are we doing this?

The goal is to provide a way for CloudCheckr customers to use their existing AWS Control Tower set up to automatically add new accounts to CloudCheckr CMx. Any new account that gets added will recieve a daily assement of CloudCheckr's 500 best practice checks identifying ways to improve cost and security.

## How do I use this?

See our [implementation guide](https://d1.awsstatic.com/Marketplace/solutions-center/downloads/AWS-CloudCheckr-Implementation-Guide.pdf) for full details.


## CloudFormation Templates

Here are the two CloudFormation templates in the templates folder.

* `cloudcheckr-controltower-integration.template.yaml` is the template to deploy the integration. It will require the s3 bucket and file with the lambda zip artifact.
* `iam-permissions-control-tower-integration.json` is the template to create the cross-account IAM role. This template takes the IAM role name as an input.

## Contributing

This is an open source project and welcomes contributions.


See our [Contributing Guide](../CONTRIBUTING.md) for more details.