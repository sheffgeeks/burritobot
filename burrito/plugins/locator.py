from irc3.plugins.command import command
import irc3
from burrito.utils import prettier_date
from datetime import datetime


ENROUTE_CMDS = ['->', '=>']
LOCATION_CMDS = ['@']
NOLOC = ['none', 'nul', 'null', 'remove', 'nowhere', 'awesome']
DTFMT = '%Y-%m-%d %H:%M:%S.%f'
LOCATION_TIMEOUT = 1209600 # 1 fortnight


@irc3.plugin
class LocatorCmds(object):
    loc_file = 'locations'

    def __init__(self, bot):
        self.bot = bot

    @command(permission='view', name='whereis')
    def cmd_whereis(self, mask, target, args):
        """Get locations

            %%whereis <user>
            %%whereis <user> <channel>
        """
        user = args['<user>']
        channel = args['<channel>']
        if not channel:
            # we'll not care to check if target is actually a channel
            channel = target
        loc_data = self.get_entry(channel, user)
        if not loc_data:
            replystr = "No idea!"
        elif loc_data['where'].lower() in NOLOC:
            replystr = "Who knows?"
        else:
            ts = datetime.strptime(loc_data['when'], DTFMT)
            replyfmtstr = "%(who)s %(atstr)s %(where)s (%(whenstr)s)"
            if (datetime.now() - ts).total_seconds() > LOCATION_TIMEOUT:
                self.bot.log.info(
                    'Location: {nick} last seen > {time}s ago'
                    .format(nick=mask.nick,
                            time=LOCATION_TIMEOUT)
                )
                replyfmtstr = "I vaguely remember %(who)s... so long ago!"
            replydict = {}
            replydict['who'] = 'you' if mask.nick == user else user
            replydict.update(loc_data)
            replydict['whenstr'] = prettier_date(ts)
            replystr = replyfmtstr % replydict
        if target.is_channel:
            return "{user}: {reply}".format(user=mask.nick, reply=replystr)
        return replystr

    @irc3.event(irc3.rfc.ACTION)
    def on_privmsg(self, mask=None, event=None, target=None, data=None):
        when = datetime.now()
        locationcmds = [cmd for cmd in LOCATION_CMDS if data.startswith(cmd)]
        enroutecmds = [cmd for cmd in ENROUTE_CMDS if data.startswith(cmd)]
        if locationcmds:
            cmd = locationcmds[0]
            atstr = '@'
        elif enroutecmds:
            cmd = enroutecmds[0]
            atstr = '=>'
        else:
            return

        where = cmd.join(data.split(cmd)[1:]).strip()
        nick = mask.lnick
        self.add_entry(target, nick, when, where, atstr)

    def add_entry(self, channel, nick, when, where, atstr='@'):
        entry = {'when': when.strftime(DTFMT),
                 'atstr': atstr,
                 'where': where}
        self.bot.log.info('adding %s %s %s to location db' % (
                          nick, atstr, where))
        self.bot.db['_'.join(['location_db', channel, nick])] = entry

    def remove_entry(self, channel, nick):
        del self.bot.db['_'.join(['location_db', channel, nick])]

    def get_entry(self, channel, nick):
        return self.bot.db['_'.join(['location_db', channel, nick])]
