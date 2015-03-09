from functools import partial
from irc3.plugins.command import command
import irc3

try:
    import dictclient
    got_dictclient = True
except:
    got_dictclient = False

MAX_DEF_LENGTH = 1000
MAX_DEFS = 1
MAX_LINELEN = 160
MAX_LINES_PER_PUBLIC_DEF = 4
normal_server = 'dict.org'
known_servers = [
    normal_server,
    'www.lojban.org',
    'dict.saugus.net',
]


def setupdictdbs():
    if not got_dictclient:
        return {}
    dbs = {}
    for s in known_servers:
        try:
            c = dictclient.Connection(s)
            sdbs = c.getdbdescs()
            for db, desc in sdbs.items():
                if db not in dbs:
                    dbs[db] = {
                        'server': s,
                        'description': desc,
                    }
        except:
            print("%(server)s is invalid or unavailable"
                  % {'server': s})
    return dbs

@irc3.plugin
class DictCmds(object):
    dbs = setupdictdbs()

    def __init__(self, bot):
        self.bot = bot
        self.translate_dbs = [k for k in self.dbs.keys() if '-' in k]
        self.other_dbs = [k for k in self.dbs.keys() if '-' not in k]

    @command(permission='view')
    def listdict(self, mask, target, args):
        """List Dictionarys

            %%listdict [<type>]
        """
        if args['<type>'] in ('trans', 'translate'):
            dbs = self.translate_dbs
        elif args['<type>'] in ('all',):
            dbs = self.other_dbs + self.translate_dbs
        else:
            dbs = self.other_dbs
        dicts = ', '.join(sorted(dbs))
        lines = irc3.utils.split_message('Dictionarys: ' + dicts, 160)
        for line in lines:
            yield line

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

    @command(permission='view')
    def define(self, mask, target, args):
        """Definition

            %%define <term>
            %%define <dict> <term>
        """
        db = args['<dict>'] if '<dict>' in args else '*'
        for d in self.db_definition(db, args['<term>']):
            yield d

    @command(permission='view', name="fulldefine", public=False)
    def fulldefine(self, mask, target, args):
        """Definition

            %%fulldefine <term>
            %%fulldefine <dict> <term>
        """
        for d in self.db_definition(args['<dict>'], args['<term>'],
                                    maxlines=0):
            yield d

    def db_definition(self, db, term, maxlines=3):
        self.bot.log.info("{name}: defining {term}".format(
            name=self.__class__.__name__, term=term))
        if db in (None, '*'):
            db = '*'
            server = normal_server
        elif db in self.dbs:
            server = self.dbs[db].get('server', None)
        else:
            yield 'Requested dictionary not found'
            return

        linecount = 0
        if server is not None:
            c = dictclient.Connection(server)
            definitions = c.define(db, term)
            if definitions:
                for defn in definitions[:MAX_DEFS]:
                    parts = self.process_definition(defn)
                    for part in parts:
                        resplit = irc3.utils.split_message(part, MAX_LINELEN)
                        for l in resplit:
                            linecount += 1
                            if maxlines and linecount > maxlines:
                                yield "..."
                                return
                            yield l
                        
            else:
                if db in self.dbs and 'description' in self.dbs[db]:
                    dstr = self.dbs[db]['description']
                else:
                    dstr = db
                yield 'No definitions found in {db}'.format(db=dstr)

    def process_definition(self, definition):
        subdefs = definition.defstr.split('\n\n')
        return [' '.join(sd.splitlines()) for sd in subdefs]

del setupdictdbs
