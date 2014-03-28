#!/usr/bin/env python3
import logging
import traceback
from datetime import datetime

from burrito.cmdsprovider import CmdsProvider


def do_command(command, target, source_user, conn_obj, connection,
               to_me=False):
    cmds = CmdsProvider.get_plugins()
    data = {'source_user': source_user,
            'target': target,
            'cmd': command.lower()
            }

    for cmd in cmds:
        # allow a plugin to play with the data before commands are
        # actually processed
        command, data = cmd.pre_process(command, conn_obj, data)
    torun = None
    for cmd in cmds:
        try:
            f, data = cmd.match_command(command, conn_obj, data)
            if torun is None:
                torun = f
        except Exception:
            logging.error(traceback.format_exc())

    # only run the one function if spoken to
    responses = torun(command, data) if to_me and torun is not None else []
    for resp in responses:
        connection.privmsg(target, resp)


def reply_to_user(data, reply):
    if isinstance(reply, str):
        head, tail = reply, []
    else:
        try:
            head, tail = reply[0], reply[1:]
        except TypeError:
            logging.warning('type error for reply to user')
            head, tail = '', []
    headoutput = [": ".join([data['source_user'], head])]
    return headoutput + tail


def extract_irc_info(command, target, source_user, conn_obj, cmd_sep=':'):
    """ used to extract some"""
    cmd = command.split(cmd_sep)[0]
    data = {'source_user': source_user,
            'target': target,
            'conn': conn_obj.connection,
            'cmd': cmd.lower(),
            }
    return cmd, data


def get_command_argstring(command, sep=':'):
    splits = command.split(sep)
    return splits[0], sep.join(splits[1:])


def prettier_date(ts):
    timeago = datetime.now() - ts
    if timeago.days > 1:
        return '%d days ago' % timeago.days
    elif timeago.seconds > 7200:
        return '%d hours ago' % int(timeago.seconds / 3600)
    elif timeago.seconds > 120:
        return '%d minutes ago' % int(timeago.seconds / 60)
    elif timeago.seconds == 1:
        return '1 second ago'
    else:
        return '%d seconds ago' % timeago.seconds
