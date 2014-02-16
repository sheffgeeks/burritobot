#!/usr/bin/env python3

from burrito.mountpoint import PluginMount


class CmdsProvider(metaclass=PluginMount):
    """Mount point for commands
    """

    def pre_process(self, command, conn_obj, data):
        return command, data

    def match_command(self, command, conn_obj, data):
        """Match commands
        """
        lcmd = command.split(':')[0].lower()
        fn = self.cmds[lcmd]['function'] if lcmd in self.cmds else None

        return fn, data

    def list_commands(self):
        """Return list of commands
        """
        return [': '.join((k, v['description']))
                for k, v in self.cmds.items() if v.get('description')]
