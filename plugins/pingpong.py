"""Returns 'pong!' if a user enters 'ping'."""

def hook():
    return r'ping'


def on_message(message):
    return 'pong!'


