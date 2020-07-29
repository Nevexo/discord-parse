# discord-parse
# A Discord data export parser
# MIT License - 2020 Cameron Fleming (Nevexo)

import click
from datetime import datetime
from parsers import user
from parsers import tracking
from parsers import guilds
from parsers import messages

u = user.Parser()
t = tracking.Parser()
g = guilds.Parser()
m = messages.Parser()

def parse():
    print("Starting parsing, this may take a moment.")
    u.parse()
    g.parse()
    m.parse()
    t.parse()
    print("Automatic parsing complete.")

def report(flags):
    parse()
    # Make some new values
    active_count = 0
    for server in m.guilds:
        server = m.guilds[server]
        if server['active']:
            active_count += 1
    
    dm_percent = round(m.dm_count / m.guild_count)

    # Create the server table
    if "NO_GUILD_TABLE" in flags:
        table = "<tr>Redacted (--no-guild-table passed)</tr>"
    else:
        table = ""
        for server in m.guilds:
            server = m.guilds[server]
            if server['active']: 
                active = "yes" 
            else: 
                active = "no"
            table += f"<tr><td>{server['name']}</td><td>{server['messages']}</td><td>{active}</td></tr>\n"

    # Gen report
    html = ""
    with open("template.html", "r+") as f:
        html = f.read()
    
    os_list = ""
    for os in t.os_uses:
        os_list += f"<li>{os} ({t.os_uses[os]} events)</li>"
    
    city_list = ""    
    if "NO_CITY_LIST" not in flags:
        for city in t.cities:
            city_list += f"<li>{city}</li>"
    else:
        city_list = "Redacted (--no-city-list passed)"

    # bit shoddy, but it works.
    html = html.replace("{GENERATED_TIMESTAMP}", str(datetime.utcnow()))
    html = html.replace("{USER_NAME}", u.name)
    html = html.replace("{USER_DISCRIM}", str(u.discrim))
    html = html.replace("{USER_ID}", str(u.id))
    html = html.replace("{SERVER_COUNT}", str(g.count))
    html = html.replace("{SERVER_ACTIVE_PERCENT}", str(round(g.count / active_count)))
    html = html.replace("{SERVER_ACTIVE}", str(active_count))
    html = html.replace("{MESSAGES_COUNT}", str(m.count))
    html = html.replace("{ORPHAN_COUNT}", str(m.orphan_guild_messages))
    html = html.replace("{FIRST_MESSAGE}", m.oldest_message['tx'])
    html = html.replace("{FIRST_MESSAGE_DATE}", str(m.oldest_message['ts']))
    html = html.replace("{MOST_COMMON_MESSAGE}", str(m.most_common_message['message']))
    html = html.replace("{MOST_COMMON_MESSAGE_COUNT}", str(m.most_common_message['count']))
    html = html.replace("{DM_TO_GUILD_PERCENT}", str(dm_percent))
    html = html.replace("{CHANNEL_COUNT}", str(len(m.channels)))
    html = html.replace("{POP_OUTS}", str(t.pop_outs_opened))
    html = html.replace("{CHANNELS_OPENED}", str(t.channels_opened))
    html = html.replace("{CALLS_JOINED}", str(t.calls_joined))
    html = html.replace("{MESSAGES_EDITED}", str(t.messages_edited))
    html = html.replace("{SESSIONS_STARTED}", str(t.sessions_started))
    html = html.replace("{LOG_IN_COUNT}", str(t.logins))
    html = html.replace("{TALKING_START_EVENTS}", str(t.speaking_start_events))
    html = html.replace("{OS_LIST}", os_list)
    html = html.replace("{CITY_LIST}", city_list)
    html = html.replace("{SERVERS_TABLE}", table)
    html = html.replace("{DISCORD_THEME}", str(u.settings['theme']))
    html = html.replace("{DISCORD_DEV_MODE}", str(u.settings['developer_mode']))
    html = html.replace("{DISCORD_GIF_AUTO}", str(u.settings['gif_auto_play']))

    with open("report.html", "w+") as f:
        f.write(html)

def intro():
    print("Welcome to discord-parse\nA simple script for pulling data out of a Discord user data export.")
    print("Some notes:\n - Data stays on your device, don't believe me? Read the code.\n" + 
          " - Time deltas are calculated by the time NOW, not when you exported your DB, so active" +
          " servers will become invalid quite quickly.\n" + 
          " - The telemetry module will still work, even if you have data usage turned off in settings (creepy, I know.)\n" + 
          " - Not all data is used, feel free to add new parsers if you find anything interesting.\n\n")

@click.group()
def cli():
    pass

@cli.command(help="Generate a HTML report of Discord export data.")
@click.option('--no-guild-table', is_flag=True, help="Don't write a guild table")
@click.option("--no-city-list", is_flag=True, help="don't write a list of visited cities")
@click.option("--no-intro", "-s", is_flag=True, help="Do not display intro message")
def html(no_guild_table, no_city_list, no_intro):
    flags = []
    if no_guild_table: flags.append("NO_GUILD_TABLE")
    if no_city_list: flags.append("NO_CITY_LIST")
    if not no_intro: intro()

    report(flags)
    print("report.html written to disk.")

if __name__ == "__main__":
    cli()
