"""Displays a randomly generated witticism from Brian Chu himself."""

import json
import random

__match__ = r"!brian"


with open('plugins/brian_corpus/cache.json', 'r') as infile:
    cache = json.load(infile)

with open('plugins/brian_corpus/phrases.json', 'r') as infile:
    phrases = json.load(infile)


def generate_phrase(phrases, cache):
    seed_phrase = []
    while len(seed_phrase) < 3:
        seed_phrase = random.choice(phrases).split()

    w1, w2 = seed_phrase[:2]
    chosen = [w1, w2]

    while "{}|{}".format(w1, w2) in cache:
        choice = random.choice(cache["{}|{}".format(w1, w2)])
        w1, w2 = w2, choice
        chosen.append(choice)

    return ' '.join(chosen)


def on_message(bot, channel, user, message):
    return '> {}'.format(generate_phrase(phrases, cache))


