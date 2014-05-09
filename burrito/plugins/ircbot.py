#!/usr/bin/env python3

from itertools import chain
import logging
import re

from irc.bot import SingleServerIRCBot
import irc.client

from burrito.commsprovider import CommsProvider
from burrito.cmdsprovider import CmdsProvider
from burrito.utils import do_command

NICK_SPLIT = re.compile('[:,]\s+')


class IRCBot(SingleServerIRCBot):
    def __init__(self, server_list, nickname, realname,
                 reconnection_interval=60, channels=None,
                 **connect_params):
        chlist = ([] if channels is None else
                  [channels] if isinstance(channels, str)
                  else channels)
        clist = chain.from_iterable([c.split(',') for c in chlist])

        self.chan_list = [c if c.startswith('#') else '#' + c for c in clist]
        super(IRCBot, self).__init__(server_list, nickname, realname,
                                     reconnection_interval, **connect_params)

    def on_nicknameinuse(self, conn, event):
        conn.nick(conn.get_nickname() + '_')

    def on_welcome(self, conn, event):
        for channel in self.chan_list:
            if irc.client.is_channel(channel):
                conn.join(channel)

    def on_ctcp(self, conn, event):
        self.do_command(event, event.arguments[0], to_me=True)

    def on_action(self, conn, event):
        self.do_command(event, event.arguments[0], to_me=True)

    def on_privmsg(self, conn, event):
        self.do_command(event, event.arguments[0], to_me=True)

    def on_pubmsg(self, conn, event):
        message = event.arguments[0]
        lnick = conn.get_nickname().lower()
        parts = NICK_SPLIT.split(message, maxsplit=1)
        head, tail = parts[0], parts[1:]

        to_me = lnick == head.lower()
        if to_me:
            message = tail[0]
        self.do_command(event, message, to_me)

    def do_command(self, event, args, to_me):
        try:
            nick = event.source.nick
        except AttributeError:
            nick = event.source.split('!~')[0]
        do_command(args, event.target, nick, self,
                   self.connection, to_me=to_me)


# IRC specific commands
class IRCCommands(CmdsProvider):
    def __init__(self):
        self.cmds = {'die': {'function': self.cmd_die,
                             'description': None}}

    def match_command(self, command, conn_obj, data):
        if isinstance(conn_obj, IRCBot):
            fn, cmd, data = super(
                IRCCommands, self).match_command(command, conn_obj, data)
            data['conn'] = conn_obj
        else:
            fn, cmd = None, None
        return fn, cmd, data

    def cmd_die(self, command, data):
        data['conn'].connection.notice(data['source_user'], "quitting")
        data['conn'].die()
        return []


class IRCCommsProvider(CommsProvider):
    name = "IRCCommsProvider"

    args = [(('--irc-server', ), {'default': "irc.freenode.net:6667",
                                  'help': "sets the irc server and port, "
                                          "defaults to irc.freenode.net:6667",
                                  'metavar': "SERVER[:PORT]"}),
            (('--irc-nick', ), {'default': "temporaryname",
                                'help': "sets the nick for the bot"}),
            (('--irc-realname', ), {'default': "BurritoBot",
                                    'help': "sets the realname of the bot"}),
            (('--irc-channels', ), {'nargs': '+',
                                    'help': "sets default channels to join"}),
            ]

    def argparse_args(self):
        return self.args

    def setup(self, options):
        serverparts = options.irc_server.split(':')
        server, port = serverparts[0], serverparts[-1]
        port = int(port) if server != port else 6667
        logging.debug("starting on %s : %d" % (server, port))
        c = IRCBot([(server, port)], options.irc_nick,
                   options.irc_realname, channels=options.irc_channels)
        c._connect()
        self.conn = c

    def run(self):
        while True:
            try:
                self.run_once()
            except UnicodeDecodeError as e:
                logging.warn(e.msg)

    def run_once(self):
        try:
            self.conn.ircobj.process_once()
        except UnicodeDecodeError as e:
            logging.warning('UnicodeDecodeError %s' % str(e))
