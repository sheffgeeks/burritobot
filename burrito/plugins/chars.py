from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user
from subprocess import PIPE, Popen, CalledProcessError


class Chars(CmdsProvider):

    def __init__(self):
        self.cmds = {
            'chars': {
                'function': self.cmd_eval,
                'description': 'count characters using wc'
            }
        }

    def cmd_eval(self, command, data):
        splitcmd = [a.strip() for a in command.split(':')]
        command = splitcmd[0]
        chars = splitcmd[1]
        proc = Popen(
            ["wc", "--chars"],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=False
        )
        try:
            outs, errs = proc.communicate(input=chars.encode('UTF-8'))
        except OSError as e:
            proc.kill()
            return reply_to_user(data, 'Subprocess error', e)
        return reply_to_user(data, outs.decode('utf-8').replace("\n", ""))
