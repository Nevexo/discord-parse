# discord-parse
# Discord data telemetry collection parser

import config
import os 
import config
import json
import click
import datetime

class Parser:
    def __init__(self):
        self.dir = os.path.join(config.EXPORT_DIR, "activity", "tns")
        self.pop_outs_opened = 0
        self.channels_opened = 0
        self.acked_messages = 0
        self.messages_edited = 0
        self.calls_joined = 0
        self.voice_chats_joined = 0
        self.sessions_started = 0
        self.logins = 0
        self.emoji_created = 0
        self.reactions = 0
        self.data_requests = 0
        self.setting_tweaks = 0
        self.os_uses = {}
        self.speaking_start_events = 0
        self.cities = []
        self.latest_event = datetime.datetime(1970,1,1,0,0,0,0)

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
                        if data['event_type'] == "join_voice_channel": self.voice_chats_joined += 1
                        if data['event_type'] == "create_emoji": self.emoji_created += 1
                        if data['event_type'] == "add_reaction": self.reactions += 1
                        if data['event_type'] == "data_request_initiated": self.data_requests += 1
                        if data['event_type'] == "update_user_settings": self.setting_tweaks += 1
                        
                        # \"2020-08-04T22:49:16.724Z\"
                        event_time_clean = data['timestamp'].replace('\\', '').replace('"', '').replace('Z', '').partition(".")[0] 
                        event_timestamp = datetime.datetime.strptime(event_time_clean, "%Y-%m-%dT%H:%M:%S")
                        self.latest_event = max(self.latest_event, event_timestamp)

                        if 'os' not in data: continue

                        if data['os'] in self.os_uses:
                            self.os_uses[data['os']] += 1
                        else:
                            self.os_uses[data['os']] = 1
                        
                        if 'city' not in data: continue

                        if data['city'] not in self.cities:
                            self.cities.append(data['city'])
