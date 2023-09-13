from mcdreforged.plugin.server_interface import PluginServerInterface


def _tr(tag: str, *args):
    _str = PluginServerInterface.get_instance().tr(f'mcdr_announcements.{tag}', *args)
    return _str
