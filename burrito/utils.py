#! /usr/bin/env python3
import logging
from burrito.cmdsprovider import CmdsProvider


def do_command(command, target, source_user, conn_obj, connection,
               to_me=False):
    cmds = CmdsProvider.get_plugins()
    data = {'source_user': source_user,
            'target': target,
            'cmd': command.lower()
            }
    torun = None
    for cmd in cmds:
        try:
            f, data = cmd.match_command(command, conn_obj, data)
            if torun is None:
                torun = f
        except Exception as e:
            logging.error(e.msg)

    # only run the one function if spoken to
    if to_me:
        if torun is not None:
            responses = torun(command, data)
            for resp in responses:
                connection.privmsg(target, resp)


def reply_to_user(data, reply):
    if isinstance(reply, str):
        head, tail = reply, []
    else:
        head, tail = reply[0], reply[1:]
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
