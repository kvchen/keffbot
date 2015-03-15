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


FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)


def read_config(filename):
    """Loads a JSON file as a dictionary."""
    with open(filename, 'r') as infile:
        return json.load(infile)


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

    keffbot = SlackBot(auth['token'], config)
    keffbot.run()


if __name__ == "__main__":
    main()


