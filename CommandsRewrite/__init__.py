# Tools
from podrum.command.Command import Command
from podrum.command.CommandManager import CommandManager
from podrum.utils.Utils import Utils
from podrum.plugin.Plugin import Plugin
from podrum.command.CommandManager import CommandManager
from podrum.lang.Base import Base
# External Modules
from zipfile import ZipFile
import json
import traceback
import time
import PluginAPI
import sys

plugin = PluginAPI.Plugins()

@plugin.command(
    description = "Stops the server."
)
def stop(sender):
    sender.sendMessage("Stopping server...")
    Plugin.unloadAll()
    sender.sendMessage("Server stopped.")
    Utils.killServer()

@plugin.command(
    description = "Says something in chat."
)
def say(sender, *, message):
    sender.sendMessage(message)

@plugin.command(
    description = "Reloads all plugins."
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
    description = 'Shows information on a plugin.'
)
def plugins(sender, *, plugin = None):
    if plugin is not None:
        if plugin in Plugin.plugins:
            _plugin = Plugin.plugins[plugin]
            sender.sendMessage(f"--- Showing info on plugin {plugin} ---")
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
    description = 'Shows help for a command.'
)
def help(sender, *, command=None):
    if command is None:
        sender.sendMessage("--- Showing help ---")
        for k, v in CommandManager.commands.items():
            sender.sendMessage("/" + str(k) + ": " + str(v.description))
        return
    command = CommandManager.getCommand(command)
    if command is not None:
        sender.sendMessage(f"--- Showing help for {command.name} ---")
        sender.sendMessage(f"{command.description}")
        sender.sendMessage(f"Usage: /{command.name} {command.usage}")
    else:
        sender.sendMessage("Invalid command.")


@plugin.command(
    description = 'Changes the game difficulty.'
)
def difficulty(sender, *, difficulty):
    if difficulty == "0" or difficulty.lower() == "peaceful":
        sender.sendMessage(f"This command does nothing right now lol")
    elif difficulty == "1" or difficulty.lower() == "easy":
        sender.sendMessage(f"This command does nothing right now lol")
    elif difficulty == "2" or difficulty.lower() == "normal":
        sender.sendMessage(f"This command does nothing right now lol")
    elif difficulty == "3" or difficulty.lower() == "hard":
        sender.sendMessage(f"This command does nothing right now lol")
    else:
        sender.sendMessage(f"{difficulty} is not a valid parameter!")

@plugin.command(
    description = 'Loads a plugin. The plugin argument is the path to the plugin (e.g. plugins/plugin.pyz)'
)
def load(sender, *, plugin):
    try:
        plugin = ZipFile(plugin, "r")
        pluginInfo = json.loads(plugin.read("plugin.json"))
        if pluginInfo["name"] in Plugin.plugins:
            sender.sendMessage("Cannot load duplicate plugin " + pluginInfo["name"])
            return
    except:
        sender.sendMessage("Invalid plugin.")
        return
    try:
        Plugin.load(plugin)
    except:
        tb = traceback.format_exc()
        sender.sendMessage.error(f"Error loading plugin {plugin}")
        for line in tb.split('\n'):
            sender.sendMessage(line)
        return
    sender.sendMessage(pluginInfo["name"] + " loaded.")

@plugin.command(
    description = 'Unloads a plugin. The plugin argument is the name of the plugin.'
)
def unload(sender, *, plugin):
    if plugin in Plugin.plugins:
        try:
            Plugin.unload(plugin)
        except:
            tb = traceback.format_exc()
            sender.sendMessage(f"Error unloading plugin {plugin}")
            for line in tb.split('\n'):
                sender.sendMessage(line)
            return
    else:
        sender.sendMessage(plugin + " is not loaded.")
        return
    sender.sendMessage(plugin + " unloaded.")

@plugin.command(
    description = 'Debugs a command.'
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
    sender.sendMessage(f"Execution completed in {end-onExcecute} seconds.")

@plugin.event()
def on_command_error(command, sender, args, error):
    if isinstance(error, PluginAPI.MissingRequiredArgument) or isinstance(error, PluginAPI.TooManyArguments):
        return sender.sendMessage(f"Usage: /{command.name} {command.usage}")
    if isinstance(error, TypeError):
        return sender.sendMessage(f"Something went wrong (you probably provided too many/too little arguments)")
    print(f"Ignoring exception in {command.name}:")
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


#core class
class CommandsRewrite:
    """ Commands Rewrite plugin class. """
    name = "Commands Rewrite"
    description = "Changes the way the default commands work, as well as adds some more."
    author = "plun1331"
    version = "v1.2"
    server = None

    
    def onLoad(self):
        pass

    def onEnable(self):
        plugin.startup()

    def onDisable(self):
        plugin.cleanup()