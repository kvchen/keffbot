import json
import logging
import websocket

from .client import SlackClient

class SlackBot(SlackClient):
    def __init__(self, name, token, plugins):
        SlackClient.__init__(self, name, token)
        self.plugins = plugins
        self.rtm_connect()


    def rtm_connect(self):
        handshake = self.call_api('rtm', 'start')
        self.ws = websocket.WebSocketApp(handshake['url'], 
            on_open=self.on_open, 
            on_message=self.on_message, 
            on_error=self.on_error,
            on_close=self.on_close)


    def send_text(self, channel, text):
        payload = {
            'id': 1, 
            'type': 'message', 
            'channel': channel, 
            'text': text, 
        }
        self.ws.send(json.dumps(payload))


    def on_open(self, ws):
        logging.info("Opened connection to Slack for {}".format(self.name))


    def on_message(self, ws, message):
        """Method that is called whenever a message is received by the 
        active websocket.
        """
        parsed = json.loads(message)

        if parsed['type'] == 'message':
            for plugin, hooks in self.plugins.items():
                response = hooks['on_message'](parsed)

                if response:
                    self.send_text(parsed['channel'], response)


    def on_error(self, ws, error):
        logging.error(error)


    def on_close(self, ws):
        logging.info("Slack closed connection for {}".format(self.name))


    def run(self):
        if not self.ws:
            self.rtm_connect()
        
        try:
            self.ws.run_forever()
        except KeyboardInterrupt as e:
            raise


