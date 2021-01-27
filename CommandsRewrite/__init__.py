# Tools
from podrum.utils.Utils import Utils
from podrum.plugin.Plugin import Plugin
from podrum.command.CommandManager import CommandManager
from podrum.lang.Base import Base
from .CommandManagerEdit import CommandManager2
# External Modules
from zipfile import ZipFile
import json
import traceback
import time
import PluginAPI
import sys

CommandManager2 = CommandManager2()
plugin = PluginAPI.Plugins()


@plugin.command(
    description="Stops the server."
)
def stop(sender):
    sender.sendMessage("Stopping server...")
    Plugin.unloadAll()
    sender.sendMessage("Server stopped.")
    Utils.killServer()


@plugin.command(
    description="Says something in chat."
)
def say(sender, *, message):
    sender.sendMessage(message)


@plugin.command(
    description="Reloads all plugins."
)
def reload(sender):
    sender.sendMessage("Reloading...")
    try:
        Plugin.unloadAll()
        Plugin.loadAll()
    except Exception as e:
        sender.sendMessage(f"Plugins could not be reloaded: {e}")
    sender.sendMessage("Reload successful!")


@plugin.command(
    description='Shows information on a plugin.',
    usage='[plugin]'
)
def plugins(sender, *, __plugin=None):
    if __plugin is not None:
        if __plugin in Plugin.plugins:
            _plugin = Plugin.plugins[__plugin]
            sender.sendMessage(f"--- Showing info on plugin {__plugin} ---")
            sender.sendMessage(_plugin["description"])
            sender.sendMessage(f"Author: {_plugin['author']}")
            sender.sendMessage(f"Version {_plugin['version']}")
            return
        else:
            sender.sendMessage("Invalid plugin.")
            return
    pluginsString = ""
    for count, pluginName in enumerate(Plugin.plugins):
        pluginsString += pluginName
        if count >= Plugin.pluginsCount:
            pluginsString += ", "
    sender.sendMessage(f"Plugins({Plugin.pluginsCount}): {pluginsString}")


@plugin.command(
    name='help',
    description='Shows help for a command.'
)
def _help(sender, *, command=None):
    if command is None:
        sender.sendMessage("--- Showing help ---")
        for k, v in CommandManager.commands.items():
            sender.sendMessage("/" + str(k) + ": " + str(v.description))
        return
    command = CommandManager2.getCommand(command)
    if command is not None:
        sender.sendMessage(f"--- Showing help for {command.name} ---")
        sender.sendMessage(f"{command.description}")
        sender.sendMessage(f"Usage: /{command.name} {command.usage}")
    else:
        sender.sendMessage("Invalid command.")


@plugin.command(
    description='Changes the game difficulty.',
    usage='<difficulty...>'
)
def difficulty(sender, *, _difficulty):
    if _difficulty == "0" or _difficulty.lower() == "peaceful":
        sender.sendMessage(f"This command does nothing right now lol")
    elif _difficulty == "1" or _difficulty.lower() == "easy":
        sender.sendMessage(f"This command does nothing right now lol")
    elif _difficulty == "2" or _difficulty.lower() == "normal":
        sender.sendMessage(f"This command does nothing right now lol")
    elif _difficulty == "3" or _difficulty.lower() == "hard":
        sender.sendMessage(f"This command does nothing right now lol")
    else:
        sender.sendMessage(f"{_difficulty} is not a valid parameter!")


@plugin.command(
    description='Loads a plugin. The plugin argument is the path to the plugin (e.g. plugins/plugin.pyz)',
    usage='<plugin...>'
)
def load(sender, *, _plugin):
    try:
        _plugin = ZipFile(_plugin)
        pluginInfo = json.loads(_plugin.read("plugin.json"))
        if pluginInfo["name"] in Plugin.plugins:
            sender.sendMessage("Cannot load duplicate plugin " + pluginInfo["name"])
            return
    except:
        sender.sendMessage("Invalid plugin.")
        return
    try:
        Plugin.load(_plugin)
    except:
        tb = traceback.format_exc()
        sender.sendMessage.error(f"Error loading plugin {_plugin}")
        for line in tb.split('\n'):
            sender.sendMessage(line)
        return
    sender.sendMessage(pluginInfo["name"] + " loaded.")


@plugin.command(
    description='Unloads a plugin. The plugin argument is the name of the plugin.',
    usage='<plugin...>'
)
def unload(sender, *, _plugin):
    if _plugin in Plugin.plugins:
        try:
            Plugin.unload(_plugin)
        except:
            tb = traceback.format_exc()
            sender.sendMessage(f"Error unloading plugin {_plugin}")
            for line in tb.split('\n'):
                sender.sendMessage(line)
            return
    else:
        sender.sendMessage(_plugin + " is not loaded.")
        return
    sender.sendMessage(_plugin + " unloaded.")


@plugin.command(
    description='Debugs a command.'
)
def debug(sender, command, *args):
    arg = [command]
    arg.extend(args)
    if command.lower() == 'debug':
        sender.sendMessage("Cannot debug the debug command.")
        return
    sender.sendMessage(f"Debugging command '{command}':")
    onExcecute = time.time()
    sender.sendMessage("")
    try:
        if CommandManager.isCommand(command):
            CommandManager.commands[command].execute(sender, arg)
        else:
            sender.sendMessage(Base.getTranslation("invalidCommand"))
    except:
        tb = traceback.format_exc()
        for line in tb.split('\n'):
            sender.sendMessage(line)
        return
    end = time.time()
    sender.sendMessage("")
    sender.sendMessage(f"Execution completed in {end - onExcecute} seconds.")


@plugin.command(
    name="list",
    description="Lists the players on the server."
)
def _list(sender):
    if len(CommandsRewrite.server.players) > 0:
        sender.sendMessage(f"{len(CommandsRewrite.server.players)} players:")
        sender.sendMessage(f"{','.join(CommandsRewrite.server.players)}")
    else:
        sender.sendMessage("0 players.")


@plugin.event()
def on_command_error(command, sender, args, error):
    if isinstance(error, PluginAPI.errors.MissingRequiredArgument) or isinstance(error,
                                                                                 PluginAPI.errors.TooManyArguments):
        return sender.sendMessage(f"Usage: /{command.name} {command.usage}")
    print(f"Ignoring exception in {command.name}:")
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


# core class
class CommandsRewrite:
    """ Commands Rewrite plugin class. """
    name = "Commands Rewrite"
    description = "Changes the way the default commands work, as well as adds some more."
    author = "plun1331"
    version = "v1.2"
    server = None

    @staticmethod
    def onLoad():
        pass

    @staticmethod
    def onEnable():
        plugin.load()

    @staticmethod
    def onDisable():
        plugin.unload()
