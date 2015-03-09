import argparse
import configparser
import itertools
import logging.config
import logging
import os

import irc3

def readConfig(filename=None, defsection='main', defaults=None):
    if defaults is None:
        defaults = {}
    config = configparser.SafeConfigParser(defaults)
    defini = 'burritobot.ini'
    locations = ['/etc/burritobot/%s' % defini,
                 '/usr/local/etc/burritobot/%s' % defini,
                 os.path.expanduser('~/.config/burritobot/%s' % defini),
                 os.path.expanduser('~/.%s' % defini)]
    if filename:
        locations.append(filename)
    config.read(locations)
    if not config.has_section(defsection):
        config.add_section(defsection)
    return config

def get_channel_list(channels=None):
    chanlist = ([] if channels is None else
                [channels] if isinstance(channels, str)
                else channels)
    clist = itertools.chain.from_iterable([c.split(',') for c in chanlist])
    return [c if c.startswith('#') else '#' + c for c in clist]

def run():
    parser = argparse.ArgumentParser(description='An irc bot')

    parser.add_argument('--config', action='store',
                        help='specify a config file to load options')
    loggroup = parser.add_mutually_exclusive_group()
    loglevels = ['debug', 'info', 'warning', 'error']
    for level in sorted(loglevels):
        loggroup.add_argument('--' + level.lower(), action='store_const',
                              const=level.upper(), default='INFO',
                              dest='loglevel',
                              help='sets logging level to %s' % level.upper())

    parser.add_argument('--irc-server', metavar='SERVER[:PORT]',
                        help='set the irc server and port')
    parser.add_argument('--irc-nick', action='store',
                        help= 'set the nick for the bot')
    parser.add_argument('--irc-channels', action='store', nargs='+',
                        help= 'sets default channels to join')
    parser.add_argument('--irc-realname', action='store', default="BurritoBot",
                        help= 'sets the realname of the bot')
    parser.add_argument('--irc-userinfo', action='store',
                        default="BurritoBot, built on irc3",
                        help= 'sets user info for the bot')

    comms_providers = []

    allargs = [comms.argparse_args() for comms in comms_providers]
    defaults = {}
    for (args, kwargs) in sorted(i for sub in allargs for i in sub):
        if 'default' in kwargs:
            optnames = [kwargs['dest']] if 'dest' in kwargs else []
            optnames.extend([s[2:].replace('-', '_') for s in args
                             if s.startswith('--')])

            if optnames:
                defaults[optnames[0]] = kwargs.pop('default')

        parser.add_argument(*args, **kwargs)

    args = parser.parse_args()
    defsection = 'main'
    config = readConfig(args.config, defsection, defaults)
    for k, v in config.items(defsection):
        if k not in args or getattr(args, k) is None:
            setattr(args, k, v)

    loglevel = getattr(logging, args.loglevel.upper())
    logging.basicConfig(level=loglevel if isinstance(loglevel, int)
                        else logging.INFO)

    logging.config.dictConfig(irc3.config.LOGGING)

    nick = args.irc_nick
    realname = args.irc_realname
    userinfo = args.irc_userinfo
    channels = get_channel_list(args.irc_channels)
    server, port = args.irc_server.split(':')

    irc3.IrcBot(
        cmd=nick + ': ',
        nick=nick, autojoins=channels,
        realname=realname,
        userinfo=userinfo,
        host=server, port=int(port), ssl=False,
        includes=[
            'irc3.plugins.core',
            'irc3.plugins.command',
            'irc3.plugins.storage',
            'burrito.plugins.dates',
            'burrito.plugins.dictionary',
            'burrito.plugins.greetings',
            'burrito.plugins.js',
            'burrito.plugins.locator',
            'burrito.plugins.pip',
            'burrito.plugins.repeats',
            'burrito.plugins.scheme',
        ],
        storage='redis://localhost:6379/10').run()

if __name__ == '__main__':
    run()
