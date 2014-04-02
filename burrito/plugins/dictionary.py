from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user

try:
    import dictclient
    got_dictclient = True
except:
    got_dictclient = False

MAX_DEF_LENGTH = 1000
MAX_DEFS = 1
normal_server = 'dict.org'
known_servers = [normal_server,
                 'www.lojban.org',
                 'dict.saugus.net',
                 ]


class DictCmds(CmdsProvider):
    def __init__(self):
        self.dbs = {}
        if got_dictclient:
            for s in known_servers:
                try:
                    c = dictclient.Connection(s)
                    sdbs = c.getdbdescs()
                    for db, desc in sdbs.items():
                        if db not in self.dbs:
                            self.dbs[db] = {
                                'server': s,
                                'description': desc,
                            }
                except:
                    print("%(server)s is invalid or unavailable"
                          % {'server': s})

        get_def = {'function':  self.cmd_definition,
                   'description': "get a definition",
                   'args': ['nick']}
        get_lst = {'function':  self.cmd_dblist,
                   'description': "get a list of dbs",
                   'args': ['nick']}
        self.cmds = {'dictionary': get_def,
                     'define': get_def,
                     'dict_list': get_lst,
                     'dictlist': get_lst,
                     'list_dict': get_lst,
                     'listdict': get_lst,
                     }

        self.cmds.update([(k, get_def) for k in self.dbs.keys()])
        self.translate_dbs = [k for k in self.dbs.keys() if '-' in k]
        self.other_dbs = [k for k in self.dbs.keys() if '-' not in k]

    def cmd_dblist(self, command, data):
        splitcmd = [a.strip() for a in command.split(':')]
        reply = []
        if 'trans' in splitcmd:
            reply.append(str(self.translate_dbs.keys))
        elif 'other' in splitcmd or 'normal' in splitcmd:
            reply.append(str(self.other_dbs))
        else:
            reply.append(str(self.other_dbs + self.translate_dbs))
        return reply_to_user(data, reply)

    def cmd_definition(self, command, data):
        splitcmd = [a.strip() for a in command.split(':')]
        command = splitcmd[0]
        defterm = splitcmd[1]
        reply = []
        if command in self.dbs:
            db = command
            server = self.dbs[command].get('server', None)
        else:
            db = '*'
            server = normal_server

        if server is not None:
            c = dictclient.Connection(server)
            definitions = c.define(db, defterm)
            if not definitions:
                reply.append('No definitions found in ' + command)
            reply.extend(self.process_definition(d)
                         for d in definitions[:MAX_DEFS])
        return reply_to_user(data, reply)

    def process_definition(self, definition):
        response = ' '.join(definition.defstr.splitlines())
        if len(response) > MAX_DEF_LENGTH:
            response = response[:MAX_DEF_LENGTH] + '[...]'
        return response
