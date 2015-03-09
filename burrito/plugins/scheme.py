from irc3.plugins.command import command
import irc3
from subprocess import PIPE, Popen, CalledProcessError
import os


@irc3.plugin
class Scheme(object):

    def __init__(self, bot):
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

    @command(permission='view', name='scheme')
    def cmd_eval(self, mask, target, args):
        """scheme: Run some scheme

            %%scheme <code> ...
        """
        code = ' '.join(args['<code>'])
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
            return 'Subprocess error: %s' % e.msg

        if errs:
            return self.truncate_output(errs, 200, 1)
        else:
            return self.truncate_output(outs, 200, 5)
