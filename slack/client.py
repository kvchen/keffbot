import logging
import requests

from .api import endpoints
from .exception import SlackError

class SlackClient(object):
    def __init__(self, name, token):
        self.name = name
        self.token = token


    def call_api(self, category, method, **params):
        params.update({'token': self.token})
        endpoint = endpoints.url(category, method)

        res = requests.get(endpoint, params=params).json()
        if not res['ok']:
            raise SlackError('API call to {}.{} failed'.format(category, 
                method))

        return res


