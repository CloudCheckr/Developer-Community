
import json
import requests
import configparser


global bearerToken
global customerNumber 
global roleIdentifier
"""
this script is designed to be used with a stack set.  
if we configure the stack set to create predictible arns we can quickly and easily credential the accounts using this script.
"roleArn": "arn:aws:iam::"+subscriptionId+":role/cc-iam-role"
Do this by adding ("RoleName" : cc-iam-role) to the cloudformation template. This removes the random string of characters appended normally at the end. 
"""
def main():
  
    config = configparser.RawConfigParser()
    config.read('config.txt')

    APIKey = config.get('config', 'APIKey')
    APISecret = config.get('config', 'APISecret')
    customerNumber = config.get('config', 'customerNumber')
    roleIdentifier = config.get('config', 'roleIdentifier')
    
    
    print("getting token")
    bearerToken = get_access_token("https://auth-us.cloudcheckr.com/auth/connect/token", APIKey, APISecret)

    getAWSAccounts(customerNumber, bearerToken, roleIdentifier)

    return

    

 
"""
    CloudCheckr API call for PutAWSCredentials
    requirements:
    predictable ARNs
        "roleArn": "arn:aws:iam::"+subscriptionId+":role/cc-iam-role"
        Do this by adding "RoleName" : cc-iam-role to the cloudformation template. This removes the random string of characters appended normally at the end. 
"""

def setAWSCred(customer_number, bearer_token, account_number, providerId, roleIdentifier):
    print("running setAWSCred")
    #print("Customer_Number: ", customer_number)
    url = "https://api-us.cloudcheckr.com/credential/v1/customers/"+str(customer_number)+"/accounts/"+account_number+"/credentials/aws"
    #print("url: ", url)
    payload = json.dumps({
      "item": {
        "regionGroup": "Commercial",
    
        "crossAccountRole": {
            "roleArn": "arn:aws:iam::"+providerId+":role/"+roleIdentifier
        },
      }
    })
    #print("Payload", payload)
    headers = {
      'Accept': 'text/plain',
      'Authorization': 'Bearer ' + bearer_token 
    }
    response = requests.request("PUT", url, headers=headers, data=payload)

    print("response: ", response.text)


def getAWSAccounts(customer_number, bearer_token, role_id):
    results = []
    print("getting all accounts")

    url = "https://api-us.cloudcheckr.com/customer/v1/customers/"+str(customer_number)+"/accounts?accountTypes=General"
    payload = None
    headers = {
      'Accept': 'text/plain',
      'Authorization': 'Bearer ' + bearer_token 
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    
    print("results: ",results)
    account_json = json.loads(response.text)
    results = account_json['items']
    #print("account_json: ", account_json)
    #print("next key:")
    nextKey = None
    if 'pagination' in account_json:
        print("pagination key is: ", account_json['pagination']['nextKey'])
        nextKey = account_json['pagination']['nextKey']

    while nextKey is not None:
        print("running while loop,  nextKey detected")
        url = "https://api-us.cloudcheckr.com/customer/v1/customers/"+str(customer_number)+"/accounts?accountTypes=General&$paginationKey="+nextKey
        payload = None
        headers = {
          'Accept': 'text/plain',
          'Authorization': 'Bearer ' + bearer_token 
        }
        response_next = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response_next.text)
        #print("response_json: ", response_json)
        if 'nextKey' in response_json['pagination']:
                nextKey = response_json['pagination']['nextKey']
                print("nextKey: ", nextKey)
        else:
            nextKey = None
        results.extend(response_json['items'])


    #loop through non credentailed accounts and call the credential after gathering external ID.
    for items in results:
        
        #print("item: ", items)
        #print("provider: ", items["provider"])
        if items["provider"] == "AWS" and items['credentialVerificationStatus'] == 'NotConfigured' or items["provider"] == "AWS" and items['credentialVerificationStatus'] == 'Failed':
            print("this item is not credentialed: ", items)
            account_number = items['id']
            external = get_external_id(customer_number, account_number, bearer_token)
            #print("external returned: ", external)
            if 'providerIdentifier' in items:
                provider_id = items['providerIdentifier']
                setAWSCred(customer_number, bearer_token, account_number, provider_id, role_id)

    



def get_external_id(customerID, accountID, bearerToken):
    region = "Commercial"
    url = "https://api-us.cloudcheckr.com/credential/v1/customers/"+str(customerID)+"/accounts/"+str(accountID)+"/external-id/aws/"+region
    payload = None
    headers = {
          'Accept': 'text/plain',
          'Authorization': 'Bearer ' + bearerToken 
        }
    credentials_response = requests.request("GET", url, headers=headers, data=payload)
    response_json = json.loads(credentials_response.text)
        
    #print("externalID json: ", response_json)
    return response_json

#Creates the bearer token
def get_access_token(url, client_id, client_secret):
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    #print("response", response)
    return response.json()["access_token"]


main()

