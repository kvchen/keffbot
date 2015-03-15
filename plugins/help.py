"""!help [command]: Prints documentation on a command provided by the bot."""

import re

__match__ = r"!help( .*)?"


def on_message(bot, message):
    command = re.findall(__match__, message['text'])[0].strip()
    
    if command:
        if command in bot.plugins:
            help_text = bot.plugins[command]['help']

            if help_text:
                return help_text
            else:
                return "No help found for command `{}`".format(command)
        else:
            return "Command `{}` not available".format(command)
    else:
        plugins = ['`{}`'.format(plugin) for plugin in sorted(bot.plugins)]
        return "Available commands: {}".format(', '.join(plugins))


