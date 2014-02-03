from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user
import random


class Greetings(CmdsProvider):
    local_data = {
        'cmds': ['hi', 'watcha', 'hello', 'oh, hai', ],
        'replies': ['hi', 'watcha', 'hello', 'oh, hai', ],
    }

    def __init__(self, *args, **kwargs):
        super(Greetings, self).__init__(*args, **kwargs)
        self.cmds = {cmd: self.cmd_greet for cmd in self.local_data['cmds']}

    def cmd_greet(self, command, data):
        return reply_to_user(data,
                             random.choice(self.local_data['replies']))

    def list_commands(self):
        # override to hide the commands
        return []
