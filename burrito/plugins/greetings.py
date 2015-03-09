import random
import irc3

@irc3.plugin
class Greetings(object):

    def __init__(self, bot):
        self.bot = bot
        self.phrases = [
            'hi', 'watcha', 'hello', 'oh hai',
        ]
        self.replies = ['{0}, %s'.format(p) for p in self.phrases]
        self.myreplies = ['%s: {0}'.format(p) for p in self.phrases]

    @irc3.event(irc3.rfc.PRIVMSG)
    def on_privmessage(self, mask=None, event=None, target=None, data=None):
        if data in self.phrases:
            self.bot.privmsg(target, random.choice(self.replies) % mask.nick)

    @irc3.event(irc3.rfc.MY_PRIVMSG)
    def on_myprivmessage(self, mask=None, event=None, target=None, data=None):
        if data in self.phrases:
            self.bot.privmsg(target, random.choice(self.myreplies) % mask.nick)
