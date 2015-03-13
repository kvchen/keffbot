import logging
import requests
import slack.api.endpoints

class Bot(object):
    def __init__(self, name, token):
        self.name = name
        self.token = token


    def loop(self):
        pass


    def _handshake(self):
        endpoint = exceptions.url('rtm', 'start')
        payload = {'token': "xoxb-4030137113-3qMRrYpJgBNLpN5NAB6deO1k"}

        response = requests.get(endpoint, params=payload)
        return response


