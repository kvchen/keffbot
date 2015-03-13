"""Echos text back to the channel.

Sample usage:
!echo [TEXT]
"""

def match(message):
    return '!echo'


def on_message(message, server):
    return message


