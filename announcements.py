import os
import threading
import time

import yaml

PLUGIN_METADATA = {
    "id": "mcdr_announcements",
    "version": "mcdr_announcements-1.0.0",
    "name": "Announcements",
    "description": "A plugin running on MCDR to send announcements regularly.",
    "author": "dodo939",
    "link": "https://github.com/yfydodo939/mcdr_announcements",
    "dependencies": {
       "mcdreforged": ">=2.0.0-alpha.1"
    }
}

timer = True
message = ""
time_interval = 0


def send(server):
    while timer:
        for t in message:
            server.say(t)
        time.sleep(time_interval)


def on_load(server, old):
    global message, time_interval
    if not os.path.exists("config//announcements_config.yml"):
        with open("config//announcements_config.yml", mode='w+', encoding='utf-8') as f:
            f.write("# The messages should be shown. Support color through add char '§'\nmessage:\n  - §6Thanks for your support!\n  - §3This plugin is developed by §e§k§ll§r§bdodo939§e§k§ll\n  - §aTo learn more please turn to ~/config/announcements_config.yml\n  # You can add more lines below\n\n# The interval time between two messages. Of course in seconds.\ntime_interval: 30  # seconds")
    with open("config//announcements_config.yml", mode='r', encoding='utf-8') as f:
        info = yaml.safe_load(f)
        time_interval = info["time_interval"]
        message = info["message"]
    sender = threading.Thread(target=send, daemon=True, args=(server,))
    sender.start()


def on_unload(server):
    global timer
    timer = False
