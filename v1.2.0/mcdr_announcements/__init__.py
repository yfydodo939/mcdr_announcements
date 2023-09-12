import os
import threading
import time

from mcdreforged.api.all import *
import yaml
from mcdr_announcements.utils import _tr

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
    server.reply(info, "§2-------- Announcements v1.2.0 --------")
    server.reply(info, RText("§7!!an§r").set_click_event(RAction.suggest_command, "!!an") + ' ' + _tr("help.help"))
    server.reply(info, RText("§7!!an enable§r").set_click_event(RAction.suggest_command, "!!an enable") + ' ' + _tr("help.enable"))
    server.reply(info, RText("§7!!an disable§r").set_click_event(RAction.suggest_command, "!!an disable") + ' ' + _tr("help.disable"))
    server.reply(info, RText("§7!!an set §6<message>§r").set_click_event(RAction.suggest_command, "!!an set ") + ' ' + _tr("help.set"))
    server.reply(info, RText("§7!!an time §6<seconds>§r").set_click_event(RAction.suggest_command, "!!an time ") + ' ' + _tr("help.time"))


def an_disable(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    if not context.has_permission_higher_than(2):
        server.reply(info, _tr("command.no_permission"))
        return
    global enabled
    enabled = False
    server.reply(info, _tr("command.off"))


def an_enable(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    if not context.has_permission_higher_than(2):
        server.reply(info, _tr("command.no_permission"))
        return
    global enabled
    enabled = True
    server.reply(info, _tr("command.on"))


def an_time(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    if not context.has_permission_higher_than(2):
        server.reply(info, _tr("command.no_permission"))
        return
    global time_interval
    interval = int(context.get_info().content.split()[2])
    if interval <= 0:
        server.reply(info, _tr("command.time_below_zero"))
        return
    time_interval = interval
    server.reply(info, _tr("command.time", interval))
    with open("config//announcements_config.yml", mode='r', encoding='utf-8') as f:
        temp = yaml.safe_load(f)
        temp["time_interval"] = interval
    with open("config//announcements_config.yml", mode='w', encoding='utf-8') as f:
        yaml.safe_dump(temp, f)


def an_set(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    if not context.has_permission_higher_than(2):
        server.reply(info, _tr("command.no_permission"))
        return
    global message
    msg = context.get_info().content.replace('&', '§')[9:].split('\\n')
    message = msg
    with open("config//announcements_config.yml", mode='r', encoding='utf-8') as f:
        temp = yaml.safe_load(f)
        temp["message"] = msg
    with open("config//announcements_config.yml", mode='w', encoding='utf-8') as f:
        yaml.safe_dump(temp, f)
    server.reply(info, _tr("command.message"))


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
            f.write(_tr("default"))
    with open("config//announcements_config.yml", mode='r', encoding='utf-8') as f:
        info = yaml.safe_load(f)
        time_interval = info["time_interval"]
        message = info["message"]
    sender = threading.Thread(target=send, daemon=True, args=(server,))
    sender.start()


def on_unload(server: ServerInterface):
    global timer
    timer = False
