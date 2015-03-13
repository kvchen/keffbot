import json
import logging
import websocket

from .client import SlackClient

class SlackBot(SlackClient):
    def __init__(self, name, token, plugins):
        SlackClient.__init__(self, name, token)
        self.plugins = plugins
        self.ws = None


    def rtm_connect(self):
        handshake = self.call_api('rtm', 'start')
        self.ws = websocket.WebSocketApp(handshake['url'], 
            on_open=self.on_open, 
            on_message=self.on_message, 
            on_error=self.on_error,
            on_close=self.on_close)


    def on_open(self, ws):
        pass


    def on_message(self, ws, message):
        parsed = json.loads(message)

        if parsed['type'] == 'message' and parsed['channel'] == 'C040YN0L6':
            payload = {
                "id": 1,
                "type": "message",
                "channel": parsed['channel'],
                "text": "pong!"
            }
            self.ws.send(json.dumps(payload))


    def on_error(self, ws, error):
        logging.error(error)


    def on_close(self, ws):
        logging.info("Slack closed connection for {}".format(self.name))


    def run(self):
        if not self.ws:
            self.rtm_connect()
        self.ws.run_forever()


