#!/usr/bin/env python3

from burrito.mountpoint import PluginMount


class CmdsProvider(metaclass=PluginMount):
    """Mount point for commands
    """

    def match_command(self, command, conn_obj, data):
        """Match commands
        """
        return self.cmds.get(command.lower()), data

    def list_commands(self):
        """Return list of commands
        """
        return [k for k in self.cmds.keys()]
