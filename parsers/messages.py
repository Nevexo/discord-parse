# discord-parse
# Messages parser (the big boi)

import click
import os
import config
import json
import csv
from datetime import datetime, timedelta

class Parser:
    def __init__(self):
        self.dir = os.path.join(config.EXPORT_DIR, "messages")
        # Stats
        self.count = 0  # Number of messages sent
        self.guild_count = 0  # Number of messages sent to giulds
        self.dm_count = 0  # Number of messages sent in a DM.
        self.messages = {}
        self.channels = []
        self.oldest_message = {}  # Oldest existing message
        self.guilds = {}  # Activity in guilds.
        self.orphan_guild_messages = 0  # Messages with no parent guild.
        self.most_common_message = {}  # Most commonly said message

    def parse(self):
        """
        Load all messages and parse them
        :return: success bool
        """

        if not os.path.exists(self.dir):
            print("[MESSAGES] No messages dir found.")
            return False

        # Read index file first
        with open(os.path.join(self.dir, "index.json"), "r+") as f:
            index = json.load(f)

        print("[MESSAGES] Indexing all messages (this gonna take a sec)")
        print(f"[MESSAGES] Message deltas are calculated from UTC ({datetime.utcnow()}).")
        # What follows is probably the worst block of code in this entire
        # script.
        with click.progressbar(index) as bar:
            for channel in bar:
                self.channels.append(channel)
                # Cycle through every channel

                # Load additional channel information
                with open(os.path.join(self.dir, channel, "channel.json")) as f:
                    channel_data = json.load(f)

                # Load messages.csv
                with open(os.path.join(self.dir, channel, "messages.csv"), encoding='utf-8') as f:
                    # Remove null bytes from csv file (thanks discord!)
                    fcsv = (line.replace('\0','') for line in f)

                    # Get messages from CSV
                    messages = csv.reader(fcsv, delimiter=',')
                    for row in messages:
                        # Cycle through every message in this channel
                        if row[0] == "ID": continue  # Probably a better way to do that but eh.

                        self.count += 1
                        if channel_data['type'] == 0: self.guild_count += 1
                        if channel_data['type'] == 1 or channel_data['type'] == 3: self.dm_count += 1

                        message = {
                            "id": row[0],
                            "ts": datetime.fromisoformat(row[1]),
                            "tx": row[2],
                            "c": channel_data
                        }

                        # Oldest message
                        if self.oldest_message == {}: self.oldest_message = message

                        if message['ts'] < self.oldest_message['ts']:
                            # New oldest message
                            self.oldest_message = message

                        # Guild activity
                        if message['c']['type'] == 0:
                            # This is a guild message
                            try:
                                g = message['c']['guild']
                                gid = g['id']
                            except:
                                self.orphan_guild_messages += 1
                                continue

                            if gid not in self.guilds: 
                                g['active'] = False
                                g['messages'] = 0
                                self.guilds[gid] = g

                            g = self.guilds[gid]

                            # Message count
                            g['messages'] += 1
                            
                            # Activity check
                            if (datetime.utcnow() - message['ts'].replace(tzinfo=None)).days <= config.IS_ACTIVE_DAYS:
                                g['active'] = True

                            self.guilds[gid] = g 

                        # Message log & counter
                        if message['tx'] in self.messages:
                            self.messages[message['tx']] += 1
                        else:
                            self.messages[message['tx']] = 1

        # Calculate most commonly said message
        n = 0
        x = ""
        for message in self.messages:
            if message == "": continue  # Skip blank messages
            if self.messages[message] > n:
                n = self.messages[message] 
                x = message

        self.most_common_message = {"message": x, "count": n}