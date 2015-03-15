"""!help [command]: Prints documentation on a command provided by the bot."""

import re

__match__ = r"!help( .*)?"


def on_message(bot, message):
    command = re.findall(__match__, message)[0].strip()
    
    if command:
        if command in bot.plugins and not bot.plugins[command]['restricted']:
            help_text = bot.plugins[command]['help']

            if help_text:
                return help_text
            else:
                return "No help found for command `{}`".format(command)
        else:
            return "Unknown command `{}`".format(command)
    else:
        plugins = []
        for plugin in sorted(bot.plugins):
            if not bot.plugins[plugin]['restricted']:
                plugins.append('`{}`'.format(plugin))

        return "Available commands: {}".format(', '.join(plugins))


