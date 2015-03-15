"""Bootstrapping program to start an instance of the bot."""

import argparse
import copy
from glob import glob
import importlib
import json
import logging
import os
import re
import sys

from slack import SlackBot


AUTH_FILE = 'auth.json'
CONFIG_FILE = 'config.json'

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PLUGIN_DIR = os.path.join(CURRENT_DIR, 'plugins')


FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)


def read_config(filename):
    """Loads a JSON file as a dictionary."""
    with open(filename, 'r') as infile:
        return json.load(infile)


def load_plugins(active_plugins):
    """Loads plugins from the PLUGIN_DIR."""
    if not os.path.isdir(PLUGIN_DIR):
        logger.exception(OSError)

    old_path = copy.deepcopy(sys.path)
    sys.path.insert(0, PLUGIN_DIR)

    plugins = {}

    for plugin_file in glob(os.path.join(PLUGIN_DIR, "[!_]*.py")):
        try:
            mod = importlib.import_module(os.path.basename(plugin_file)[:-3])
            mod_name = mod.__name__

            # Skip the plugin if not active
            if mod_name not in active_plugins:
                logger.debug("Skipping inactive plugin {}".format(mod_name))
                continue
            else:
                logger.debug("Loading plugin {}".format(mod_name))
                plugins[mod_name] = {}

            # Check if the plugin has a regular expression for matching
            if '__match__' in dir(mod):
                p_match = mod.__match__
            else:
                p_match = r'!{0} (.*)'.format(mod_name)
            plugins[mod_name]['match'] = re.compile(p_match)

            # Add the docstring to help if it exists
            if mod.__doc__:
                plugins[mod_name]['help'] = mod.__doc__

            # Locate all methods that begin with 'on_'
            for hook in re.findall('on_(\w+)', ' '.join(dir(mod))):
                hook_name = 'on_{}'.format(hook)
                hook_fn = getattr(mod, hook_name)

                plugins[mod_name][hook_name] = hook_fn
                logger.debug("Attached {} hook for {}".format(hook_name, 
                    mod_name))

        except Exception as e:
            logger.exception(e)
            logger.warn("Import failed for {}, plugin not loaded".format(
                mod))

    sys.path = old_path
    return plugins


def main():
    parser = argparse.ArgumentParser(
        description="handles messages for a bot instance in Slack chat.")
    parser.add_argument("-d", "--debug", action="store_true", 
        help="enable debugging output")
    args = parser.parse_args()

    if args.debug:
        logger.info("Debugging output enabled")
        logger.setLevel(logging.DEBUG)

    auth = read_config(AUTH_FILE)
    config = read_config(CONFIG_FILE)

    plugins = load_plugins(config['active_plugins'])

    keffbot = SlackBot(auth['token'], plugins)
    keffbot.run()


if __name__ == "__main__":
    main()


