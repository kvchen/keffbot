"""ping: Returns `pong!`"""

phrases = {
    'ping': 'pong!', 
    'ayyy': ':fu:', 
}

__match__ = r'(?i){}'.format('|'.join(phrases))


def on_message(bot, channel, user, message):
    msg_lower = message.lower()
    if msg_lower in phrases:
        return phrases[msg_lower]


