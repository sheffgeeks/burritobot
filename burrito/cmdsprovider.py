#!/usr/bin/env python3

import functools

from burrito.mountpoint import PluginMount


# taken from the PythonDecoratorLibrary page
def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


class CmdsProvider(metaclass=PluginMount):
    """Mount point for commands
    """

    def _generate_alias_commands(self):
        cmdmap = {}
        for cname, cdict in self.cmds.items():
            cmdmap[cname] = cname
            cmdmap.update({a: cname for a in cdict.get('aliases', [])})
        self.cmdmap = cmdmap

    def pre_process(self, command, conn_obj, data):
        return command, data

    def match_command(self, command, conn_obj, data):
        """Match commands
        """
        splitcmd = command.split(':')
        lcmd = splitcmd[0].lower()
        tcmd = lcmd.translate({c: '' for c in b"'?!; "})

        self._generate_alias_commands()
        thecmd = self.cmdmap.get(lcmd, self.cmdmap.get(tcmd))

        (fn, modcmd) = (
            self.cmds[thecmd]['function'],
            ':'.join([thecmd] + splitcmd[1:])) if thecmd else (None, None)
        return fn, modcmd, data

    def list_commands(self):
        """Return list of commands
        """
        return [': '.join((k, v['description']))
                for k, v in self.cmds.items()
                if v.get('description') and not v.get('nolist')]
