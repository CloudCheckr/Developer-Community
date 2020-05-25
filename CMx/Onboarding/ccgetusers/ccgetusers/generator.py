import subprocess
import sys
import re
import logging
import requests

log = logging.getLogger(__name__)


class GenerateToken:
    def __init__(self, cc_endpoint, client_id, client_secret):
        """
        Uses OAuth 2.0 to get the Bearer Token
        """
        api_url = cc_endpoint + "/auth/connect/token"

        client = {'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret,
                'scope': 'api'
        }

        response = requests.post(api_url, data=client)

        if "access_token" in response.json():
            self._token = response.json()["access_token"]
    
    @property
    def token(self):
        return self._token
