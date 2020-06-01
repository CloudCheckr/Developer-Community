from ccgetusers.generator import GenerateToken
from ccgetusers.customerid import CustomerId
from ccgetusers.users import Users
import sys


def main():
    if len(sys.argv) < 4:
        print('Must provide CloudCheckr CMx auth endpoint, client id and access key')
        print('ccgetusers <cloudcheckr endpoint> <client id> <access key>')
        sys.exit(-1)
    else:
        cc_endpoint = sys.argv[1]
        client_id = sys.argv[2]
        client_secret = sys.argv[3]
        token = GenerateToken(cc_endpoint=cc_endpoint, client_id=client_id, client_secret=client_secret)
        token = token.token
        customer_id = CustomerId(cc_endpoint=cc_endpoint, token=token)
        customer_id = customer_id.customer_id
        users = Users(cc_endpoint=cc_endpoint, token=token, customer_id=customer_id)
        return users.users
