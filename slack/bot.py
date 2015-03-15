import copy
from glob import glob
import importlib
import json
import logging
import os
import time
import re
import sys

from .client import SlackClient

RATE_LIMIT = 1.5
logger = logging.getLogger('root')

class SlackBot(SlackClient):
    def __init__(self, token, config):
        SlackClient.__init__(self, token)

        self.admin = config.get('admin', None)
        self.plugin_info = config.get('plugin_info')
        self.plugin_dir = config.get('plugin_dir')

        self.load_plugins()
        logger.info("Loaded plugins")

        self.connect()
        logger.info("Connected to Slack team channel")

        self.admin_id = None
        if self.admin:
            for user in self.team.users:
                if user['name'] == self.admin:
                    self.admin_id = user['id']
                    logger.info("Found admin ID: {}".format(self.admin_id))
                    break


    def send_text(self, channel, text):
        payload = {
            'id': 1, 
            'type': 'message', 
            'channel': channel, 
            'text': text, 
        }
        self.ws.send(json.dumps(payload))


    def on_event(self, ws, message):
        """Method that is called whenever an event message is received by the 
        active websocket.
        """
        parsed = json.loads(message)

        # Catch confirmations of sent messages
        if 'reply_to' in parsed:
            pass

        # If a normal event is received
        elif 'type' in parsed and parsed['type'] == 'message':
            self.on_message(parsed)


    def on_message(self, event):
        channel_id = event['channel']
        user_id = event['user']
        is_admin = user_id == self.admin_id

        for plugin_name, info in self.plugins.items():
            message = event['text']
            if info['match'].match(message):
                logger.debug('Message matched by {}'.format(plugin_name))

                channel_info = self.call_api('channels', 'info', 
                    channel=channel_id)['channel']

                # Check black/whitelisting filters
                if 'whitelist' in info:
                    if self.team.name not in info['whitelist']:
                        logger.debug("Team not whitelisted for command '{}'"
                            .format(plugin_name))
                        break

                    whitelisted = info['whitelist'][self.team.name]
                    if channel_info['name'] not in whitelisted:
                        logger.debug("Channel not whitelisted for command '{}'"
                            .format(plugin_name))
                        break

                if 'blacklist' in info:
                    if self.team.name in info['blacklist']:
                        blacklisted = info['blacklist'][self.team.name]
                        if channel_info['name'] in blacklisted:
                            logger.debug("Channel blacklisted for command '{}'"
                                .format(plugin_name))
                            break

                # Allow only admins to call restricted commands
                if not info['restricted'] or is_admin:
                    response = info['module'].on_message(self, channel_id, 
                        user_id, message)

                    if response:
                        self.send_text(event['channel'], response)
                        time.sleep(RATE_LIMIT)

                break


    def load_plugins(self):
        if not os.path.isdir(self.plugin_dir):
            logger.exception(OSError)

        old_path = copy.deepcopy(sys.path)
        sys.path.insert(0, self.plugin_dir)

        self.plugins = {}
        for plugin_file in glob(os.path.join(self.plugin_dir, "[!_]*.py")):
            try:
                mod_file = os.path.basename(plugin_file)[:-3]
                mod = importlib.import_module(mod_file)

                mod_name = mod.__name__

                # Skip the plugin if not active
                if mod_name not in self.plugin_info:
                    logger.debug("No config found for {}".format(mod_name))
                    continue
                elif not self.plugin_info[mod_name]['enabled']:
                    logger.debug("Skipping inactive plugin {}".format(mod_name))
                    continue

                logger.debug("Loading plugin {}".format(mod_name))
                self.plugins[mod_name] = {
                    'restricted': self.plugin_info[mod_name]['restricted']
                }

                # Add in filters
                for lst in ('whitelist', 'blacklist'):
                    if lst in self.plugin_info[mod_name]:
                        lst_filter = self.plugin_info[mod_name][lst]
                        self.plugins[mod_name][lst] = lst_filter

                # Check if the plugin has a regular expression for matching
                if '__match__' in dir(mod):
                    p_match = mod.__match__
                else:
                    p_match = r'!{0} (.*)'.format(mod_name)
                self.plugins[mod_name]['match'] = re.compile(p_match)

                # Add the docstring to help if it exists
                if mod.__doc__:
                    self.plugins[mod_name]['help'] = mod.__doc__

                # Store the module and its commands
                self.plugins[mod_name]['module'] = mod

            except Exception as e:
                logger.exception(e)
                logger.warn("Import failed for {}, plugin not loaded".format(
                    mod))

        sys.path = old_path


