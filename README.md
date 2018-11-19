![CloudCheckr Success Center](https://raw.githubusercontent.com/alecrajeev/Developer-Community/master/logo/cc_logo2.png)
# Welcome to the CloudCheckr Development Community!

Hi! Welcome to the CloudCheckr Development community! This is a repository of scripts, tools or otherwise that can help you quickly integrate CloudCheckr using the native **API**.

If you're new to CloudCheckr and just getting started. Please check out our **Getting Started Guide** on our Success portal: [Lets go!](https://success.cloudcheckr.com/)

## What is this?

This GitHub developer community is a culmination of scripts, tools and otherwise that have been used by CloudCheckr staff and customers to quickly connect internal tools to CloudCheckr OR quickly configure CloudCheckr based on their business needs.

## Why are we doing this?

Over the last few years we have noticed an increasing number of customers integrating CloudCheckr via our API directly into their own internal tools. 

Additionally, we have seen the need to help customers rapidly deploy new accounts, configurations and users into CloudCheckr via the API. 

In order to help expedite this initiative, we created this GitHub repository and compiled a curated number of scripts, tools and other items in order to help jump start a developers work.

## How do I use this?

This is a public GitHub repository, please feel free to fork it or pull down the code directly into your GIT client of choice.

Content is separated by category as it relates to CloudCheckr as a product and implies how scripts could be used per product module.

In order to get started with the API and to access your API key, please review the following instructions: https://support.cloudcheckr.com/api-cli-and-setup/

The currently published scripts are written in python 3 and use the [requests](http://docs.python-requests.org/en/master/) module for making API calls. In order to run the scripts, you will have to enter in the API key to the command line. The 64 character string is a API key that is used to connect to the CloudCheckr API. Some scripts will have other command line arguments that are written to the command line as well or variables that can be configured in the script such as account name.

For data processing and analysis the json, [numpy](http://www.numpy.org/), and [pandas](https://pandas.pydata.org/) libraries are used for certain scripts.

```
python get_ec2_instances.py 0000000000000000000000000000000000000000000000000000000000000000
```

## Contributing

This is an open source project and welcomes contributions. See our [Contributing Guide](CONTRIBUTING.md) for more details.


## Example use case

1. A number of Cloud Resellers and MSPs have their own internal tools to help create a Quarterly Business Review document or dashboard. Using the CloudCheckr API you can pull out a end customers cloud spend data across 1-N accounts as well as their forecast and any custom reporting you have made for them via Advanced Grouping.
2. An MSP may be onboarding new customers and have created a set number of Budget Alerts and Security Alerts based on their service offering. You can easily script the Alerts via the CloudCheckr API to enable easy onboarding of your customers configuration into the system.
3. If your security team likes to keep an audit history of system changes, alerts or compliance initiatives within a internal system to your company, you can use the CloudCheckr API to pull this data into your system. Easily pull down Best Practice Checks, Change Monitoring and Total Compliance data points to ingest into an external repository.