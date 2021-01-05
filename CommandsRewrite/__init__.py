# Tools
from podrum.command.Command import Command
from podrum.command.CommandManager import CommandManager
from podrum.utils.Utils import Utils
from podrum.plugin.Plugin import Plugin
from podrum.command.CommandManager import CommandManager
# Default Commands
from podrum.command.vanilla.DifficultyCommand import DifficultyCommand
from podrum.command.vanilla.HelpCommand import HelpCommand
from podrum.command.vanilla.PluginsCommand import PluginsCommand
from podrum.command.vanilla.ReloadCommand import ReloadCommand
from podrum.command.vanilla.SayCommand import SayCommand
from podrum.command.vanilla.StopCommand import StopCommand
# Rewritten Commands
from .commands import StopCommandR
from .commands import SayCommandR
from .commands import ReloadCommandR
from .commands import PluginsCommandR
from .commands import HelpCommandR
from .commands import DifficultyCommandR
from .commands import LoadPlugin
from .commands import UnloadPlugin

#core class
class CommandsRewrite:
    """ Commands Rewrite plugin class. """
    name = "Commands Rewrite"
    description = "Changes the way the default commands work, as well as adds some more."
    author = "plun1331"
    version = "v1.0"
    server = None

    def __init__(self):
        self.commands = [StopCommandR(),
                         SayCommandR(),
                         HelpCommandR(),
                         ReloadCommandR(),
                         PluginsCommandR(),
                         DifficultyCommandR(),
                         LoadPlugin(),
                         UnloadPlugin()]
        self.default_commands_str = ["stop",
                                "say",
                                "reload",
                                "plugins",
                                "help",
                                "difficulty"]
        self.commands_str = ["stop",
                        "say",
                        "reload",
                        "plugins",
                        "help",
                        "difficulty",
                        "load",
                        "unload"]
        self.default_commands = [DifficultyCommand(),
                            HelpCommand(),
                            PluginsCommand(),
                            ReloadCommand(),
                            SayCommand(),
                            StopCommand()]

    
    def onLoad(self):
        """ Called when the plugin is loaded. """
        pass

    def onEnable(self):
        """ Removes the default commands and replaces them with better commands, as well as adds some new commands. """
        for command in self.default_commands_str:
            CommandManager.deleteCommand(command)
        for command in self.commands:
            CommandManager.registerCommand(command)

    def onDisable(self):
        """ Removes the commands in the plugin, and reinstates the default commands. """
        for command in self.commands_str:
            CommandManager.deleteCommand(command)
        for command in self.default_commands:
            CommandManager.registerCommand(command)