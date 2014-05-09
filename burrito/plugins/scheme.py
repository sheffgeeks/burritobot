from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user
from subprocess import PIPE, Popen, CalledProcessError
import os


class Scheme(CmdsProvider):

    def __init__(self):
        self.cmds = {
            'scheme': {
                'function': self.cmd_eval,
                'description': 'Run some Scheme',
                'aliases': ['scm']
            }
        }
        dirname = os.path.abspath(os.path.dirname(__file__))
        self.bin = os.path.join(
            dirname, '../../scripts/scheme-sandbox/sandboxed'
        )

    def truncate_output(self, data, maxcols, maxlines):
        lines = data.decode('utf-8').split("\n")
        logs = [x for x in lines[:-1] if x]
        result = lines[-1]
        output = []
        for x in logs[:maxlines]:
            if len(x) > maxcols:
                output.append(x[:maxcols] + '...')
            else:
                output.append(x)
        if len(logs) > maxlines:
            output.append('<... console output truncated ...>')
        if len(result) > maxcols:
            output.append(result[:maxcols] + '...')
        else:
            output.append(result)
        return output

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

        if errs:
            return reply_to_user(data, self.truncate_output(errs, 200, 1))
        else:
            return reply_to_user(data, self.truncate_output(outs, 200, 5))
