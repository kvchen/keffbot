"""Stores a list of phrases and matches them to other phrases. Returns the
corresponding phrase when a user enters in a matching phrase.
"""

phrases = {
    'ping': 'pong!', 
    'he\'s losing his mind': 'and I\'m reaping all the benefits', 
}

def on_message(message):
    msg_lower = message['text'].lower()
    if msg_lower in phrases:
        return phrases[msg_lower]


