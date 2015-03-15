"""Stores a list of phrases and matches them to other phrases. Returns the
corresponding phrase when a user enters in a matching phrase.
"""

phrases = {
    'ping': 'pong!', 
}

__match__ = r'|'.join(phrases.keys())


def on_message(bot, message):
    msg_lower = message['text'].lower()
    if msg_lower in phrases:
        return phrases[msg_lower]


