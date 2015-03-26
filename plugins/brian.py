"""!brian: Displays a randomly generated witticism from Brian Chu himself."""

import json
import random

__match__ = r"!brian"

attribution = [
    "salad master", 
    "esquire", 
    "the one and only", 
    "startup enthusiast", 
    "boba king", 
    "not-dictator", 
    "normal citizen", 
    "ping-pong expert"
]


with open('plugins/brian_corpus/phrases.json', 'r') as infile:
    phrases = json.load(infile)

with open('plugins/brian_corpus/cache.json', 'r') as infile:
    cache = json.load(infile)


def generate_phrase(phrases, cache, max_length=40):
    seed_phrase = []
    while len(seed_phrase) < 2:
        seed_phrase = random.choice(phrases).split()

    w1, = seed_phrase[:1]
    chosen = [w1]

    while w1 in cache and len(chosen)<max_length:
        w1 = random.choice(cache[w1])
        chosen.append(w1)

    return ' '.join(chosen)


def on_message(bot, channel, user, message):
    return '> {} ~ Brian Chu, {}'.format(generate_phrase(phrases, cache), 
        random.choice(attribution))


