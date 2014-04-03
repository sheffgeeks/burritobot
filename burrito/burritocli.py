import argparse
import configparser
import logging
import os

from burrito.commsprovider import CommsProvider
from burrito.plugins import *


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

    comms_providers = CommsProvider.get_plugins()

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

    for comms in comms_providers:
        comms.setup(args)

    while True:
        for comms in comms_providers:
            comms.run_once()

if __name__ == "__main__":
    run()
