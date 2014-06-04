from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user
from subprocess import PIPE, STDOUT, Popen, CalledProcessError
import os
import logging


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
            dirname, '../../scripts/js-sandbox/sandboxed.js'
        )
        self.cwd = os.path.dirname(self.bin)

    def cmd_eval(self, command, data):
        splitcmd = [a.strip() for a in command.split(':')]
        command = splitcmd[0]
        code = splitcmd[1]
        output = self.actual_eval(code)
        return reply_to_user(data, output)

    def actual_eval(self, js):
        logging.debug("Running `%s` in %s" % (self.bin, self.cwd))
        proc = Popen(
            [self.bin],
            cwd=self.cwd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT,
            shell=False
        )
        try:
            outs, errs = proc.communicate(input=js.encode('UTF-8'))
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
        return output

if __name__ == '__main__':
    cmd = JS()
    import sys
    print("\n".join(cmd.actual_eval(sys.stdin.read())))
