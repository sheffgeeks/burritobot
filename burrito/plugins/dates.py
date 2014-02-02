from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user
from datetime import datetime


class DateCmds(CmdsProvider):
    formats = {'date': '%x',
               'time': '%X',
               'datetime': '%x %X',
               'isotime': None,
               'isodatetime': None,
               'isodate': None,
               }

    def __init__(self, *args, **kwargs):
        self.cmds = {cmd: self.cmd_date for cmd in self.formats.keys()}

    def cmd_date(self, command, data):
        lcmd = command.lower()
        dt = datetime.now()
        fmt = self.formats.get(lcmd)
        if fmt:
            output = dt.strftime(fmt)
        elif lcmd == 'isotime':
            output = dt.time().isoformat()
        elif lcmd == 'isodate':
            output = dt.date().isoformat()
        elif lcmd == 'isodatetime':
            output = dt.isoformat()
        return reply_to_user(data, output)
