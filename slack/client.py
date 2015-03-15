import logging
import requests
import websocket

from .api import endpoints
from .exception import SlackError
from .team import SlackTeam

class SlackClient(object):
    def __init__(self, token):
        self.token = token


    def call_api(self, category, method, **params):
        params.update({'token': self.token})
        endpoint = endpoints.url(category, method)

        res = requests.get(endpoint, params=params).json()
        if not res['ok']:
            raise SlackError('API call to {}.{} failed'.format(category, 
                method))

        return res


    def connect(self):
        handshake = self.call_api('rtm', 'start')
        self.id = handshake['self']['id']
        self.name = handshake['self']['name']
        self.team = SlackTeam(
            id=handshake['team']['id'], 
            name=handshake['team']['name'], 
            users=handshake['users'], 
            channels=handshake['channels'],
            groups=handshake['groups'],
            bots=handshake['bots'])

        self.ws = websocket.WebSocketApp(handshake['url'], 
            on_open=self.on_open, 
            on_message=self.on_event, 
            on_error=self.on_error,
            on_close=self.on_close)


    def on_event(self, ws, message):
        pass


    def on_error(self, ws, error):
        logging.error(error)


    def on_close(self, ws):
        logging.info("Slack closed connection for {}".format(self.name))


    def on_open(self, ws):
        logging.info("Opened connection to Slack for {}".format(self.name))


    def run(self):
        try:
            self.ws.run_forever()
        except KeyboardInterrupt as e:
            raise