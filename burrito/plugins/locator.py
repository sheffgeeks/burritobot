from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user, prettier_date
from datetime import datetime
import shelve


ENROUTE_CMDS = ['->', '=>']
LOCATION_CMDS = ['@']
NOLOC = ['none', 'nul', 'null', 'remove', 'nowhere', 'awesome']


class LocatorCmds(CmdsProvider):
    loc_file = 'locations'

    def __init__(self):
        whereis = {'function':  self.cmd_whereis,
                   'description': "attempts to tell you where someone is",
                   'args': ['nick']}
        whereiseveryone = {
            'function': self.cmd_whereiseveryone,
            'description': "reports all known last locations",
            'aliases': ['whereiseverybody', 'whereseveryone',
                        'whereseverybody'],
        }
        self.cmds = {'whereis': whereis,
                     'whereiseveryone': whereiseveryone,
                     }

    def cmd_whereiseveryone(self, command, data):
        try:
            loc_data = shelve.open(self.loc_file)
            asker = data['source_user']
            reply = [
                '_{0}_: {1} ({2})'.format(nick, loc[-1]['where'],
                                          prettier_date(loc[-1]['when']))
                for nick, loc in loc_data.items()
                if nick != asker and loc[-1]['where'].lower() not in NOLOC
            ]
            if not reply:
                if asker in loc_data:
                    reply = ['You are the only one I know about!']
                else:
                    reply = ['Nobody has told me anything!']
        except:
            reply = ['(shh.. someone made me do something wrong!)']
        finally:
            loc_data.close()
        return reply_to_user(data, reply)

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
            elif loc_data[who][-1]['where'].lower() in NOLOC:
                replystr = "Who knows?"
            else:
                replyfmtstr = "%(who)s %(atstr)s %(where)s (%(whenstr)s)"
                replydict = {'who': who}
                replydict.update(loc_data[who][-1])
                replydict['whenstr'] = prettier_date(replydict['when'])
                replystr = replyfmtstr % replydict
        except:
            reply = ['(shh.. someone made me do something wrong!)']
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
