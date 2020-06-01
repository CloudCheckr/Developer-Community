import subprocess
import sys
import re
import logging
import requests

log = logging.getLogger(__name__)


class Users:
    def __init__(self, cc_endpoint, token, customer_id):
        """
        Gets the list of users
        """
        api_url = cc_endpoint + "/auth/v1/customers/" + customer_id + "/users"
        authorization_value = "Bearer " + token

        response = requests.get(api_url, headers={"Authorization": authorization_value})

        self._users = response.json()
    
    @property
    def users(self):
        return self._users
