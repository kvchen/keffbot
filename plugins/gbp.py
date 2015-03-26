"""!gbp [user]: A record of good boy points."""

import re
import json


with open('plugins/gbp_data/gbp.json', 'r') as infile:
    gbp = json.load(infile)


__match__ = r'(!gbp <@(.*)>)|(<@(.*)>[\+,\-]{2})'



def write_gbp():
    with open('plugins/gbp_data/gbp.json', 'w') as outfile:
        json.dump(gbp, outfile)


def increment(user):
    get_gbp(user)
    gbp[user] += 1

    write_gbp()
    return gbp[user]


def decrement(user):
    get_gbp(user)    
    gbp[user] -= 1

    write_gbp()
    return gbp[user]


def get_gbp(user):
    if user not in gbp:
        gbp[user] = 0
        write_gbp()
    
    return gbp[user]


def on_message(bot, channel, user, message):
    match = [s.strip() for s in re.findall(__match__, message)[0]]
    _, check_user, _, give_user = match

    if check_user:
        user_info = bot.call_api('users', 'info', user=check_user)
        if not user_info['ok']:
            return "No such user."

        username = user_info['user']['name']
        user_id = user_info['user']['id']

        return "*{}*: {} _gbp_".format(username, get_gbp(user_id))

    elif give_user:
        user_info = bot.call_api('users', 'info', user=give_user)

        if not user_info['ok']:
            return "No such user."

        if user == give_user:
            decrement(user)
            return

        increment_user = message[-2:] == '++'

        # Increment or decrement the receiving user as necessary
        if increment_user:
            increment(give_user)
        else:
            if give_user == bot.admin_id:
                decrement(user)
            decrement(give_user)

