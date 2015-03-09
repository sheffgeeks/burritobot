from irc3.plugins.command import command
import irc3
from subprocess import PIPE, STDOUT, Popen, CalledProcessError
import os
import logging


@irc3.plugin
class JS(object):

    def __init__(self, bot):
        self.bot = bot
        dirname = os.path.abspath(os.path.dirname(__file__))
        self.bin = os.path.join(
            dirname, '../../scripts/js-sandbox/sandboxed.js'
        )
        self.cwd = os.path.dirname(self.bin)

    @command(permission='view', name='js')
    def cmd_eval(self, mask, target, args):
        """js: Run some javascript

            %%js <code> ...
        """
        code = ' '.join(args['<code>'])
        output = self.actual_eval(code)
        for line in output:
            yield line

    def actual_eval(self, js):
        self.bot.log.info("JS: Running `%s` in %s" % (self.bin, self.cwd))
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
