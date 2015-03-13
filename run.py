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

logging.basicConfig(level=logging.INFO)


CONFIG_FILE = 'config.json'

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PLUGIN_DIR = os.path.join(CURRENT_DIR, 'plugins')


def read_config():
    """Loads the bot configuration from a JSON file as a dictionary."""
    with open(CONFIG_FILE, 'r') as infile:
        return json.load(infile)


def load_plugins(active_plugins):
    """Loads plugins from the PLUGIN_DIR."""
    if not os.path.isdir(PLUGIN_DIR):
        logging.exception(OSError)

    active = set(active_plugins)
    old_path = copy.deepcopy(sys.path)
    sys.path.insert(0, PLUGIN_DIR)

    hooks = {}

    for plugin in glob(os.path.join(PLUGIN_DIR, "[!_]*.py")):
        try:
            mod = importlib.import_module(os.path.basename(plugin)[:-3])
            mod_name = mod.__name__

            if mod_name not in active:
                continue

            logging.debug("Loading plugin {}".format(mod_name))

            hooks[mod_name] = {}

            # Locate all methods that begin with 'on_'
            for hook in re.findall("on_(\w+)", " ".join(dir(mod))):
                fhook_name = "on_{}".format(hook)
                fhook = getattr(mod, fhook_name)

                hooks[mod_name][fhook_name] = fhook
                logging.debug("Attached {} hook for {}".format(fhook_name, 
                    mod_name))

            if mod.__doc__:
                hooks[mod_name]['help'] = mod.__doc__

        except Exception as e:
            print(e)
            logging.warn("Import failed for {}, plugin not loaded".format(
                plugin))

    sys.path = old_path
    return hooks


def main():
    parser = argparse.ArgumentParser(
        description="handles messages for a bot instance in Slack chat.")
    parser.add_argument("-d", "--debug", action="store_true", 
        help="enable debugging output")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    config = read_config()
    plugins = load_plugins(config['active_plugins'])

    keffbot = SlackBot(config['name'], config['token'], plugins)
    keffbot.run()


if __name__ == "__main__":
    main()


