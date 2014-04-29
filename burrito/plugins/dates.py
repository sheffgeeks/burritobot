from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user
from datetime import datetime


class DateCmds(CmdsProvider):
    formats = {'date': {'format': '%x',
                        'description': 'Server locale date format'},
               'time': {'format': '%X',
                        'description': 'Server locale time format'},
               'datetime': {'format': '%x %X',
                            'description': 'Server locale date time format'},
               'isotime': {'format': None,
                           'description': 'ISO 8601 format time'},
               'isodatetime': {'format': None,
                               'description': 'ISO 8601 format date time'},
               'isodate': {'format': None,
                           'description': 'ISO 8601 format date'},
               }

    def __init__(self, *args, **kwargs):
        self.cmds = {cmd: {'function': self.cmd_date,
                           'description': v['description']}
                     for cmd, v in self.formats.items()}

    def cmd_date(self, command, data):
        lcmd = command.lower()
        dt = datetime.now()
        fmt = self.formats.get(lcmd, {}).get('format')
        if fmt:
            output = dt.strftime(fmt)
        elif lcmd == 'isotime':
            output = dt.time().isoformat()
        elif lcmd == 'isodate':
            output = dt.date().isoformat()
        elif lcmd == 'isodatetime':
            output = dt.isoformat()
        return reply_to_user(data, output)
