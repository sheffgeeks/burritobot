import argparse
import logging

from burrito.commsprovider import CommsProvider
from burrito.plugins import *


def run():
    parser = argparse.ArgumentParser(description='An irc bot')

    loggroup = parser.add_mutually_exclusive_group()
    loglevels = ['debug', 'info', 'warning', 'error']
    for level in sorted(loglevels):
        loggroup.add_argument('--' + level.lower(), action='store_const',
                              const=level.upper(), default='INFO',
                              dest='loglevel',
                              help='sets logging level to %s' % level.upper())

    comms_providers = CommsProvider.get_plugins()

    allargs = [comms.argparse_args() for comms in comms_providers]
    for (args, kwargs) in sorted(i for sub in allargs for i in sub):
        parser.add_argument(*args, **kwargs)

    args = parser.parse_args()
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
