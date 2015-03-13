"""Bootstrapping program to start an instance of the bot."""

import argparse
import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PLUGIN_DIR = os.path.join(CURRENT_DIR, 'plugins')



def main():
    parser = argparse.ArgumentParser(
        description="attaches an instance of keffbot to the Slack chat")
    parser.add_argument("-d", "--debug", action="store_true", 
        help="enable debugging output")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)



if __name__ == "__main__":
    main()


