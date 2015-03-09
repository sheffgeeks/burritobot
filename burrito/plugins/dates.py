from irc3.plugins.command import command
from datetime import datetime
from functools import partial
import irc3

@irc3.plugin
class Date(object):
    def __init__(self, bot):
        self.bot = bot
        self.cmds = {
            'date': '%x',
            'time': '%X',
            'datetime': '%x %X',
            'isodate': '%Y-%m-%d',
            'isotime': '%H:%M:%S',
            'isodatetime': '%Y-%m-%dT%H:%M:%S',
        }
        self._date = partial(self.process_dt_cmds, 'date')
        self._time = partial(self.process_dt_cmds, 'time')
        self._datetime = partial(self.process_dt_cmds, 'datetime')
        self._isodate = partial(self.process_dt_cmds, 'isodate')
        self._isotime = partial(self.process_dt_cmds, 'isotime')
        self._isodatetime = partial(self.process_dt_cmds, 'isodatetime')

    @command(permission='view')
    def date(self, mask, target, args):
        """Date

            %%date
        """
        return self._date(mask, target, args)

    @command(permission='view')
    def time(self, mask, target, args):
        """Time

            %%time
        """
        return self._time(mask, target, args)

    @command(permission='view')
    def datetime(self, mask, target, args):
        """Datetime

            %%datetime
        """
        return self._datetime(mask, target, args)

    @command(permission='view')
    def isodate(self, mask, target, args):
        """Isodate

            %%isodate
        """
        return self._isodate(mask, target, args)

    @command(permission='view')
    def isotime(self, mask, target, args):
        """Isotime

            %%isotime
        """
        return self._isotime(mask, target, args)

    @command(permission='view')
    def isodatetime(self, mask, target, args):
        """Isodatetime

            %%isodatetime
        """
        return self._isodatetime(mask, target, args)

    def process_dt_cmds(self, cmd, mask, target, args):
        fmt = self.cmds[cmd]
        dt = datetime.now()
        self.bot.log.info(fmt)
        strtime = dt.strftime(fmt)
        if target.is_channel:
            return "{user}: {time}".format(user=mask.nick, time=strtime)
        return dt.strftime(fmt)
