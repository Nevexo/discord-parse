# discord-parse
# user information parser

import config
import json
import os

class Parser:
    def __init__(self):
        self.dir = os.path.join(config.EXPORT_DIR, "account")
        self.id = 0
        self.name = ""
        self.discrim = ""
        self.settings = {}
        self.notes = {}
        self.mobile = False

    def parse(self):
        """
        Doesn't do a whole lot lol"""

        with open(os.path.join(self.dir, "user.json")) as f:
            data = json.load(f)

        self.id = data['id']
        self.name = data['username']
        self.discrim = data['discriminator']
        self.settings = data['settings']
        self.notes = data['notes']
        self.mobile = data['has_mobile']

        # k done lol
        return True