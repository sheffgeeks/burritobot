from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user, prettier_date
from datetime import datetime
import shelve


ENROUTE_CMDS = ['->', '=>']
LOCATION_CMDS = ['@']


class LocatorCmds(CmdsProvider):
    loc_file = 'locations'

    def __init__(self):
        whereis = {'function':  self.cmd_whereis,
                   'description': "attempts to tell you where someone is",
                   'args': ['nick']}
        self.cmds = {'whereis': whereis,
                     'where is': whereis,
                     }

    def cmd_whereis(self, command, data):
        splitcmd = [a.strip() for a in command.split(':')]
        who = splitcmd[1]
        reply = []
        if who == data['source_user']:
            reply.append("Don't you know where you are?")

        try:
            loc_data = shelve.open(self.loc_file)
            if who not in loc_data:
                replystr = "No idea!"
            else:
                replyfmtstr = "%(who)s %(atstr)s %(where)s (%(whenstr)s)"
                replydict = {'who': who}
                replydict.update(loc_data[who][-1])
                replydict['whenstr'] = prettier_date(replydict['when'])
                replystr = replyfmtstr % replydict
        finally:
            reply.append(replystr)
            loc_data.close()

        return reply_to_user(data, reply)

    def add_entry(self, nick, when, where, atstr='@'):
        entry = {'when': when,
                 'atstr': atstr,
                 'where': where.strip()}
        try:
            loc_data = shelve.open(self.loc_file)
            if nick not in loc_data:
                loc_data[nick] = [entry]
            elif len(loc_data[nick]) < 5:
                tmp_data = loc_data[nick]
                tmp_data.append(entry)
                loc_data[nick] = tmp_data
            else:
                loc_data[nick] = loc_data[nick][1:] + [entry]
        finally:
            loc_data.close()

    def splitcmd(self, command, op, data):
        if command.startswith(op):
            return data['source_user'], command.replace(op, '', 1)
        return None, None

    def pre_process(self, command, conn_obj, data):
        nick, location, atstr = None, None, '->'
        for op in ENROUTE_CMDS:
            nick, location = self.splitcmd(command, op, data)
            if nick is not None:
                break
        if nick is None:
            for op in LOCATION_CMDS:
                nick, location = self.splitcmd(command, op, data)
                if nick is not None:
                    atstr = '@'
                    break
        if nick is not None:
            self.add_entry(nick, datetime.now(), location, atstr)
        return command, data
