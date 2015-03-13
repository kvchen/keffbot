"""Returns 'pong!' if a user enters 'ping'."""


def on_message(message):
    if message['text'] == 'ping':
        return 'pong!'


