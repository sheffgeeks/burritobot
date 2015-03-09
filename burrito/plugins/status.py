from irc3.plugins.command import command
import irc3
from burrito.utils import prettier_date
from datetime import datetime


STATUS_CMDS = ['is']
PAST_MAP = {'is': 'was'}
YOU_MAP = {'is': 'are', 'was': 'were'}
NOSTAT = ['none', 'null', 'remove']
DTFMT = '%Y-%m-%d %H:%M:%S.%f'
STATUS_TIMEOUT = 1209600 # 1 fortnight


@irc3.plugin
class StatusCmds(object):

    def __init__(self, bot):
        self.bot = bot

    @command(permission='view', name='status')
    def cmd_status(self, mask, target, args):
        """Get locations

            %%status <user>
            %%status <user> <channel>
        """
        user = args['<user>']
        channel = args['<channel>']
        if not channel:
            # we'll not care to check if target is actually a channel
            channel = target
        stat_data = self.get_entry(channel, user)
        if not stat_data:
            replystr = "No idea!"
        elif stat_data['status'].lower() in NOSTAT:
            replystr = "Who knows?"
        else:
            ts = datetime.strptime(stat_data['when'], DTFMT)
            replyfmtstr = "%(who)s %(statstr)s %(status)s (%(whenstr)s)"
            if (datetime.now() - ts).total_seconds() > STATUS_TIMEOUT:
                self.bot.log.info(
                    'Status: {nick} last seen > {time}s ago'
                    .format(nick=mask.nick,
                            time=STATUS_TIMEOUT)
                )
                replyfmtstr = "I vaguely remember %(who)s... so long ago!"
            replydict = {}
            replydict['who'] = 'you' if mask.nick == user else user
            replydict.update(stat_data)
            if replydict['who'] == 'you' and replydict['statstr'] in YOU_MAP:
                replydict['statstr'] = YOU_MAP[replydict['statstr']]
            replydict['whenstr'] = prettier_date(ts)
            replystr = replyfmtstr % replydict
        if target.is_channel:
            return "{user}: {reply}".format(user=mask.nick, reply=replystr)
        return replystr

    @irc3.event(irc3.rfc.ACTION)
    def on_privmsg(self, mask=None, event=None, target=None, data=None):
        when = datetime.now()
        statcmds = [cmd for cmd in STATUS_CMDS if data.startswith(cmd)]
        if statcmds:
            cmd = statcmds[0]
            statstr = PAST_MAP.get(cmd, cmd)
        else:
            return

        status = statstr.join(data.split(cmd)[1:]).strip()
        nick = mask.nick
        self.add_entry(target, nick, when, status, statstr)

    def add_entry(self, channel, nick, when, status, statstr='is'):
        entry = {'when': when.strftime(DTFMT),
                 'statstr': statstr,
                 'status': status}
        self.bot.log.info('adding %s %s %s to status db' % (
                          nick, statstr, status))
        self.bot.db['_'.join(['status_db', channel, nick])] = entry

    def remove_entry(self, channel, nick):
        del self.bot.db['_'.join(['status_db', channel, nick])]

    def get_entry(self, channel, nick):
        return self.bot.db['_'.join(['status_db', channel, nick])]
