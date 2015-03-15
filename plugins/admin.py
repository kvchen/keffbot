import binascii
import git
import sys
import os
import logging

logger = logging.getLogger('root')

__match__ = r"!update|!reload"

def on_message(bot, channel, user, message):
    requires_reload = message == '!reload'

    if message == '!update':
        local = git.Repo(os.getcwd())
        origin = git.remote.Remote(local, 'origin')
        head = local.heads[0]

        logger.info("Updating from origin repository")
        for pull_info in origin.pull():
            if head.commit == pull_info.commit:
                bot.send_text(channel, "`{}` is already up-to-date!".format(
                    bot.name))
                break

            requires_reload = True
            commit_hash = binascii.hexlify(pull_info.commit.binsha).decode()
            commit_message = pull_info.commit.message.strip()

            bot.send_text(channel, "*Fast-forwarding* to `{}`".format(
                commit_hash))
            logger.debug("Fast-forwarding to {}".format(commit_hash))

            bot.send_text(channel, "*Latest commit*: `{}`".format(
                commit_message))
            logger.debug("Latest commit: {}".format(commit_message))
    
    if requires_reload:
        bot.send_text(channel, "_Reloading...see you on the other side!_")
        python = sys.executable
        os.execl(python, python, *sys.argv)

