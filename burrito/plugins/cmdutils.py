import irc3
from irc3.plugins.command import Commands

@irc3.extend
def getcmds(bot, *args):
    return bot.plugins.get(Commands).keys()
