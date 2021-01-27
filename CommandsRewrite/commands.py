# Tools
import json
import time
import traceback
# External Libraries
from zipfile import ZipFile

from podrum.command.Command import Command
from podrum.command.CommandManager import CommandManager
from podrum.lang.Base import Base
from podrum.plugin.Plugin import Plugin
from podrum.utils.Utils import Utils

# Rewritten Commands
from CommandsRewrite.CommandManager import CommandManager2


class StopCommandR(Command):
    """ Remade stop command. """

    def __init__(self, name="", description="", usage=""):
        super().__init__("stop", "Stops the server.")
        self.usage = ""

    @staticmethod
    def execute(sender, args):
        """ Executes the command. """
        sender.sendMessage("Stopping server...")
        Plugin.unloadAll()
        sender.sendMessage("Server stopped.")
        Utils.killServer()


class SayCommandR(Command):
    """ Remade say command. """

    def __init__(self, name="", description="", usage=""):
        super().__init__("say", "Says something in chat.")
        self.usage = "<message>"

    @staticmethod
    def execute(sender, args):
        """ Executes the command. """
        if len(args) > 1:
            sender.sendMessage(" ".join(args[1:]))
        else:
            sender.sendMessage("say <message>")


class ReloadCommandR(Command):
    """ Remade reload command. """

    def __init__(self, name="", description="", usage=""):
        super().__init__("reload", "Reloads all plugins.")
        self.usage = ""

    @staticmethod
    def execute(sender, args):
        """ Executes the command. """
        sender.sendMessage("Reloading...")
        try:
            Plugin.unloadAll()
            Plugin.loadAll()
        except Exception as e:
            sender.sendMessage(f"Plugins could not be reloaded: {e}")
        sender.sendMessage("Reload successful!")


class PluginsCommandR(Command):
    """ Remade plugins command. """

    def __init__(self, name="", description=""):
        super().__init__("plugins", "Shows plugin information.")
        self.usage = "[plugin]"

    @staticmethod
    def execute(sender, args):
        """ Executes the command. """
        if len(args) > 1:
            if " ".join(args[1:]) in Plugin.plugins:
                plugin = Plugin.plugins[" ".join(args[1:])]
                sender.sendMessage(f"--- Showing info on plugin {' '.join(args[1:])} ---")
                sender.sendMessage(plugin["description"])
                sender.sendMessage(f"Author: {plugin['author']}")
                sender.sendMessage(f"Version {plugin['version']}")
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


class HelpCommandR(Command):
    """ Remade help command. """

    def __init__(self, name="", description="", usage=""):
        super().__init__("help", "Shows help for a command.")
        self.usage = "[command]"

    @staticmethod
    def execute(sender, args):
        """ Executes the command. """
        if len(args) == 1:
            sender.sendMessage("--- Showing help ---")
            for k, v in CommandManager.commands.items():
                sender.sendMessage("/" + k + ": " + v.description)
            return
        command = CommandManager2.getCommand(" ".join(args[1:]))
        if command is not None:
            sender.sendMessage(f"--- Showing help for {command.name} ---")
            sender.sendMessage(f"{command.description}")
            sender.sendMessage(f"Usage: /{command.name} {command.usage}")
        else:
            sender.sendMessage("Invalid command.")


class DifficultyCommandR(Command):
    """ Remade difficulty command. """

    def __init__(self, name="", description="", usage=""):
        super().__init__("difficulty", "Changes the difficulty.")
        self.usage = "<difficulty>"

    @staticmethod
    def execute(sender, args):
        """ Executes the command. """
        if len(args) == 2:
            if args[1] == "0" or args[1].lower() == "peaceful":
                sender.sendMessage(f"This command does nothing right now lol")
            elif args[1] == "1" or args[1].lower() == "easy":
                sender.sendMessage(f"This command does nothing right now lol")
            elif args[1] == "2" or args[1].lower() == "normal":
                sender.sendMessage(f"This command does nothing right now lol")
            elif args[1] == "3" or args[1].lower() == "hard":
                sender.sendMessage(f"This command does nothing right now lol")
            else:
                sender.sendMessage(f"{args[1]} is not a valid parameter!")
        else:
            sender.sendMessage("Usage: /difficulty <difficulty>")


# New Commands
class LoadPlugin(Command):
    """ Load command. """

    def __init__(self, name="", description="", usage=""):
        super().__init__("load",
                         "Loads a plugin. The Plugin argument is the path to the plugin (e.g. plugins/plugin.pyz)")
        self.usage = "<plugin>"

    @staticmethod
    def execute(sender, args):
        """ Executes the command. """
        if len(args) > 1:
            try:
                plugin = ZipFile(" ".join(args[1:]), "r")
                pluginInfo = json.loads(plugin.read("plugin.json"))
                if pluginInfo["name"] in Plugin.plugins:
                    sender.sendMessage("Cannot load duplicate plugin " + pluginInfo["name"])
                    return
            except:
                sender.sendMessage("Invalid plugin.")
                return
            try:
                Plugin.load(" ".join(args[1:]))
            except:
                tb = traceback.format_exc()
                sender.sendMessage.error(f"Error loading plugin {' '.join(args[1:])}")
                for line in tb.split('\n'):
                    sender.sendMessage(line)
                return
            sender.sendMessage(pluginInfo["name"] + " loaded.")
        else:
            sender.sendMessage("Usage: /load <plugin>")


class UnloadPlugin(Command):
    """ Unload command. """

    def __init__(self, name="", description="", usage=""):
        super().__init__("unload", "Unloads a plugin. The plugin argument is the name of the plugin.")
        self.usage = "<plugin...>"

    @staticmethod
    def execute(self, sender, args):
        """ Executes the command. """
        if len(args) > 1:
            if " ".join(args[1:]) in Plugin.plugins:
                try:
                    Plugin.unload(" ".join(args[1:]))
                except:
                    tb = traceback.format_exc()
                    sender.sendMessage(f"Error unloading plugin {' '.join(args[1:])}")
                    for line in tb.split('\n'):
                        sender.sendMessage(line)
                    return
            else:
                sender.sendMessage(" ".join(args[1:]) + " is not loaded.")
                return
            sender.sendMessage(" ".join(args[1:]) + " unloaded.")
        else:
            sender.sendMessage("Usage: /unload <plugin>")


class DebugCommand(Command):
    """ Debug command. """

    def __init__(self, name="", description="", usage=""):
        super().__init__("debug", "Debugs a command.")
        self.usage = "<command> [args...]"

    @staticmethod
    def execute(sender, args):
        """ Executes the command. """
        if len(args) > 1:
            args = args[1:]
            command = args[0]
            if command.lower() == 'debug':
                sender.sendMessage("Cannot debug the debug command.")
                return
            sender.sendMessage(f"Debugging command '{' '.join(args)}':")
            onExcecute = time.time()
            sender.sendMessage("")
            try:
                if CommandManager.isCommand(command):
                    CommandManager.commands[command].execute(sender, args)
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
        else:
            sender.sendMessage("Usage: /debug <command> [args...]")


class ListCommand(Command):
    """ List command. """

    def __init__(self, plugin, name="", description="", usage=""):
        super().__init__("list", "Lists the players on the server.")
        self.plugin = plugin
        self.usage = ""

    def execute(self, sender, args):
        """ Executes the command. """
        if len(self.plugin.server.players) > 0:
            sender.sendMessage(f"{len(self.plugin.server.players)} players:")
            sender.sendMessage(f"{','.join(self.plugin.server.players)}")
        else:
            sender.sendMessage("0 players.")
