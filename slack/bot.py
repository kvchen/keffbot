import json
import logging
import time

from .client import SlackClient

RATE_LIMIT = 1
logger = logging.getLogger('root')

class SlackBot(SlackClient):
    def __init__(self, token, plugins):
        SlackClient.__init__(self, token)
        self.plugins = plugins
        self.connect()


    def send_text(self, channel, text):
        payload = {
            'id': 1, 
            'type': 'message', 
            'channel': channel, 
            'text': text, 
        }
        self.ws.send(json.dumps(payload))


    def on_message(self, ws, message):
        """Method that is called whenever a message is received by the 
        active websocket.
        """
        parsed = json.loads(message)

        # Catch confirmations of sent messages
        if 'reply_to' in parsed:
            pass

        # If a normal event is received
        elif 'type' in parsed:
            if parsed['type'] == 'message':
                for plugin, hooks in self.plugins.items():
                    if hooks['match'].match(parsed['text']):
                        logger.debug('Message matched by {}'.format(plugin))
                        response = hooks['on_message'](self, parsed)

                        if response:
                            self.send_text(parsed['channel'], response)
                            time.sleep(RATE_LIMIT)

                        break


