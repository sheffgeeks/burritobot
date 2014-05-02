from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user
import random


class Greetings(CmdsProvider):
    respond_to_public = True

    local_data = {
        'cmds': ['hi', 'watcha', 'hello', 'oh, hai', ],
        'replies': ['hi', 'watcha', 'hello', 'oh, hai', ],
    }

    def __init__(self):
        self.cmds = {cmd: {'function': self.cmd_greet}
                     for cmd in self.local_data['cmds']}

    def cmd_greet(self, command, data):
        return reply_to_user(data,
                             random.choice(self.local_data['replies']))
