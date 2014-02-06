from itertools import chain
from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user


class HelpCommands(CmdsProvider):
    def __init__(self):
        self.cmds = {'commands': {'function': self.cmd_list,
                                  'description': None},
                     'help': {'function': self.cmd_help_cmd,
                              'description': 'get help for a cmd',
                              'usage': 'usage: %(nick)s: help: <command>',
                              'args': ['command']}}

    def _get_cmd_list(self):
        return sorted(list(chain.from_iterable(
            [c.list_commands() for c in CmdsProvider.get_plugins()])))

    def _get_cmd_dict(self):
        result = {}
        for p in CmdsProvider.get_plugins():
            result.update(p.cmds)
        return result

    def cmd_list(self, command, data):
        cmds = self._get_cmd_list()
        return reply_to_user(data, cmds)

    def cmd_help_cmd(self, command, data):
        splitcmd = [a.strip() for a in command.split(':')]
        _, args = splitcmd[0], splitcmd[1:]
        cmds = self._get_cmd_dict()
        if len(args) == 1 and args[0] in cmds:
            cmd = cmds[args[0]]
            reply = cmd.get('help', cmd.get('description', None))
            if not reply:
                reply = "No help found for %s" % cmd
        else:
            reply = self.cmds['help']['usage'] % {'nick':
                                                  data['conn']._nickname}
        return reply_to_user(data, reply)
