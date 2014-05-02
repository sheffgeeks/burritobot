from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user
from subprocess import PIPE, Popen, CalledProcessError
import os


class JS(CmdsProvider):

    def __init__(self):
        self.cmds = {
            'js': {
                'function': self.cmd_eval,
                'description': 'Run some JavaScript'
            }
        }
        dirname = os.path.abspath(os.path.dirname(__file__))
        self.bin = os.path.join(
            dirname, '../../scripts/sandbox-cli/sandboxed.js'
        )

    def cmd_eval(self, command, data):
        splitcmd = [a.strip() for a in command.split(':')]
        command = splitcmd[0]
        code = splitcmd[1]
        proc = Popen(
            [self.bin],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=False
        )
        try:
            outs, errs = proc.communicate(input=code.encode('UTF-8'))
        except OSError as e:
            proc.kill()
            return reply_to_user(data, 'Subprocess error', e)

        lines = outs.decode('utf-8').split("\n")
        logs = lines[:-1]
        result = lines[-1]
        output = logs[:5]
        if len(logs) > 5:
            output.append('<... console output truncated ...>')
        output.append(result)
        return reply_to_user(data, output)
