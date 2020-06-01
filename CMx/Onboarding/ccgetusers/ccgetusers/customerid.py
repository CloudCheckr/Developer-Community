import subprocess
import sys
import re
import logging
import requests

log = logging.getLogger(__name__)


class CustomerId:
    def __init__(self, cc_endpoint, token):
        """
        Gets the Customer id
        """
        api_url = cc_endpoint + "/auth/v1/token/info"
        authorization_value = "Bearer " + token

        response = requests.get(api_url, headers={"Authorization": authorization_value})

        if "customerId" in response.json():
            self._customer_id = response.json()["customerId"]

    @property
    def customer_id(self):
        return self._customer_id
