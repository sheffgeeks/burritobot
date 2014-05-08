#!/usr/bin/env python3
import logging
import traceback
from datetime import datetime
from time import sleep

from burrito.cmdsprovider import CmdsProvider


def do_command(command, target, source_user, conn_obj, connection,
               to_me=False):
    cmds = CmdsProvider.get_plugins()
    data = {'source_user': source_user,
            'target': target,
            'cmd': command.lower(),
            'to_me': to_me
            }

    for cmd in cmds:
        # allow a plugin to play with the data before commands are
        # actually processed
        command, data = cmd.pre_process(command, conn_obj, data)
    torun = None
    for cmd in cmds:
        try:
            f, c, data = cmd.match_command(command, conn_obj, data)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            respond_to_public = getattr(cmd, "respond_to_public", False)

            # will only run function if spoken to or respond_to_public is True
            if (torun is None) and (to_me or respond_to_public):
                torun, thecmd = f, c

    responses = torun(thecmd, data) if torun is not None else []
    for i, resp in enumerate(responses):
        sleep(0.1 * i)
        connection.privmsg(target, resp)


def chop_by_length(data, chunksize):
    size = len(data)
    return [data[i:i + chunksize] for i in range(0, size, chunksize)]


def reply_to_user(data, reply):
    if isinstance(reply, str):
        head, tail = reply, []
    else:
        try:
            head = reply[0] if len(reply) else ''
            tail = reply[1:] if len(reply) > 1 else []
        except TypeError:
            logging.warning('type error for reply to user')
            head, tail = '', []
    headoutput = [": ".join([data['source_user'], head])]
    alloutput = headoutput + tail
    output = []
    for line in alloutput:
        output.extend(chop_by_length(line, 256))
    return output


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
