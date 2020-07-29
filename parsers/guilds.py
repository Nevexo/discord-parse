# discord-parse
# guild data parser

import os
import config
import json

class Parser:
    def __init__(self):
        self.data = {}
        self.dir = os.path.join(config.EXPORT_DIR, "servers")
        self.count = 0

    def parse(self):
        """
        Parse all files into the self.data object
        ready for processing
        :return: Result
        """

        if not os.path.exists(self.dir):
            print("[GUILDS] Cannot find servers directory in exports.")
            return False

        if len(os.listdir(self.dir)) == 0:
            print("[GUILDS] No guild files found.")
            return False

        with open(os.path.join(self.dir, "index.json"), "r+") as f:
            data = json.load(f)
            f.close()

        self.count = len(data)