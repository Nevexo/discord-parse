# discord-parse
# Discord data telemetry collection parser

import config
import os 
import config
import json
import click

class Parser:
    def __init__(self):
        self.dir = os.path.join(config.EXPORT_DIR, "activity", "tns")
        self.pop_outs_opened = 0
        self.channels_opened = 0
        self.acked_messages = 0
        self.messages_edited = 0
        self.calls_joined = 0
        self.sessions_started = 0
        self.logins = 0
        self.os_uses = {}
        self.speaking_start_events = 0
        self.cities = []

    def parse(self):
        """
        Loads the tns telemetry export"""

        for telemfile in os.listdir(self.dir):
            with open(os.path.join(self.dir, telemfile), encoding='utf-8') as f:
                lines = f.readlines()

                print(f"Processing {len(lines)} telemetry events... (zuckerberg 100)")
                with click.progressbar(lines) as bar:
                    for telemobject in bar:
                        data = json.loads(telemobject)
                        
                        if data['event_type'] == "open_popout": self.pop_outs_opened += 1
                        if data['event_type'] == "join_call": self.calls_joined += 1
                        if data['event_type'] == "ack_messages": self.acked_messages += 1
                        if data['event_type'] == "channel_opened": self.channels_opened += 1
                        if data['event_type'] == "message_edited": self.messages_edited += 1
                        if data['event_type'] == "session_start": self.sessions_started += 1
                        if data['event_type'] == "start_speaking": self.speaking_start_events += 1

                        if 'os' not in data: continue

                        if data['os'] in self.os_uses:
                            self.os_uses[data['os']] += 1
                        else:
                            self.os_uses[data['os']] = 1
                        
                        if 'city' not in data: continue

                        if data['city'] not in self.cities:
                            self.cities.append(data['city'])
