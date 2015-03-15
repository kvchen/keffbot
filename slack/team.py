class SlackTeam(object):
    def __init__(self, id, name, users, channels, groups, bots):
        self.id = id
        self.name = name
        self.users = users
        self.channels = channels
        self.groups = groups
        self.bots = bots