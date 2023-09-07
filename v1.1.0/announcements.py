import os
import threading
import time

from mcdreforged.api.all import *
import yaml

PLUGIN_METADATA = {
    "id": "mcdr_announcements",
    "version": "1.1.0",
    "name": "Announcements",
    "description": "A plugin running on MCDR to send announcements regularly.",
    "author": "dodo939",
    "link": "https://github.com/yfydodo939/mcdr_announcements",
    "dependencies": {
       "mcdreforged": ">=2.0.0-alpha.1"
    }
}

timer = True
enabled = False
message = []
time_interval = 0


def send(server: ServerInterface):
    while timer:
        if enabled:
            for t in message:
                server.say(t)
        time.sleep(time_interval)


def an(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    server.reply(info, "§2-------- Announcements v1.1.0 --------")
    server.reply(info, RText("§7!!an§r").set_click_event(RAction.suggest_command, "!!an") + " Show this help message list")
    server.reply(info, RText("§7!!an enable§r").set_click_event(RAction.suggest_command, "!!an enable") + " Enable the timed announcement")
    server.reply(info, RText("§7!!an disable§r").set_click_event(RAction.suggest_command, "!!an disable") + " Disable the timed announcement")
    server.reply(info, RText("§7!!an set §6<message>§r").set_click_event(RAction.suggest_command, "!!an set ") + " Set the content of announcement. '\\n' for next line and '&' for the color text")
    server.reply(info, RText("§7!!an time §6<seconds>§r").set_click_event(RAction.suggest_command, "!!an time ") + " Set the interval time (seconds/time)")


def an_disable(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    if not context.has_permission_higher_than(2):
        server.reply(info, "§4Sorry, but you have no permission to do that! ")
        return
    global enabled
    enabled = False
    server.reply(info, "§2[Announcements] The announcement turns off. ")


def an_enable(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    if not context.has_permission_higher_than(2):
        server.reply(info, "§4Sorry, but you have no permission to do that! ")
        return
    global enabled
    enabled = True
    server.reply(info, "§2[Announcements] The announcement turns on. ")


def an_time(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    if not context.has_permission_higher_than(2):
        server.reply(info, "§4Sorry, but you have no permission to do that! ")
        return
    global time_interval
    interval = int(context.get_info().content.split()[2])
    if interval <= 0:
        server.reply(info, "§4The interval cannot be below zero! ")
        return
    time_interval = interval
    server.reply(info, "§2Showing announcement every " + str(interval) + "s")
    with open("config//announcements_config.yml", mode='r', encoding='utf-8') as f:
        temp = yaml.safe_load(f)
        temp["time_interval"] = interval
    with open("config//announcements_config.yml", mode='w', encoding='utf-8') as f:
        yaml.safe_dump(temp, f)


def an_set(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    if not context.has_permission_higher_than(2):
        server.reply(info, "§4Sorry, but you have no permission to do that! ")
        return
    global message
    msg = context.get_info().content.replace('&', '§')[9:].split('\\n')
    message = msg
    with open("config//announcements_config.yml", mode='r', encoding='utf-8') as f:
        temp = yaml.safe_load(f)
        temp["message"] = msg
    with open("config//announcements_config.yml", mode='w', encoding='utf-8') as f:
        yaml.safe_dump(temp, f)
    server.reply(info, "§2The message has been modified! ")


def on_load(server: ServerInterface, old):
    # commands
    builder = SimpleCommandBuilder()
    builder.command("!!an", an)
    builder.command("!!an disable", an_disable)
    builder.command("!!an enable", an_enable)
    builder.command("!!an time <interval>", an_time)
    builder.command("!!an set <message>", an_set)
    
    builder.arg("interval", Integer)
    builder.arg("message", GreedyText)
    
    builder.register(server)
    
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


def on_unload(server: ServerInterface):
    global timer
    timer = False
