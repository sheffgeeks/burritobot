from itertools import chain
from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user


class ListCommands(CmdsProvider):
    def __init__(self):
        self.cmds = {'commands': self.cmd_list, }

    def cmd_list(self, command, data):
        # collect commands
        cmds = list(chain.from_iterable(
            [c.list_commands() for c in CmdsProvider.get_plugins()]))
        return reply_to_user(data, cmds)
