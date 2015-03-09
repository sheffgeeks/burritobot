from irc3.plugins.command import command
from datetime import datetime
from functools import partial
import irc3

@irc3.plugin
class Date(object):
    def __init__(self, bot):
        self.bot = bot

    @command(permission='view')
    def datetime(self, mask, target, args):
        """Datetime

            %%datetime [<fmt>] ...
        """
        fmt = ' '.join(args['<fmt>']) if args['<fmt>'] else '%Y-%m-%dT%H:%M:%S'
        dt = datetime.now()
        self.bot.log.info(fmt)
        strtime = dt.strftime(fmt)
        if target.is_channel:
            return "{user}: {time}".format(user=mask.nick, time=strtime)
        return dt.strftime(fmt)
