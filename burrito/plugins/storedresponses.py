import random
import shelve
import shlex

from burrito.cmdsprovider import CmdsProvider

EVENTUAL_RESP_FILE = 'eventualresponses'
IMMEDIATE_RESP_FILE = 'immediateresponses'

IMMEDIATE_CMD = 'learncanned'
DELAYED_CMD = 'learndelayed'


class AddResponses(CmdsProvider):
    eventual_resp_file = EVENTUAL_RESP_FILE
    immediate_resp_file = IMMEDIATE_RESP_FILE

    def __init__(self):
        self.cmds = {
            IMMEDIATE_CMD: {
                'function': self.cmd_add_entry,
                'args': ['key', 'response', 'probability']},
            DELAYED_CMD: {
                'function': self.cmd_add_entry,
                'args': ['key', 'response', 'probability']},
        }

    def cmd_add_entry(self, command, data):
        splitcmd = command.split(':')
        cmd, therest = splitcmd[0], ':'.join(splitcmd[1:])
        args = shlex.split(therest)

        if len(args) < 2:
            return ["not enough information - at least a trigger and a "
                    "response is required"]
        elif len(args) == 2:
            key, responses, probability = args[0], args[1:], None
        else:
            key = args[0].strip()
            try:
                responses, probability = args[1:-1], float(args[-1])
            except:
                responses, probability = args[1:], None

        entry = {
            'responses': set(responses),
        }

        if cmd == IMMEDIATE_CMD:
            respfile = IMMEDIATE_RESP_FILE
            defprob = 1.0
        else:
            respfile = EVENTUAL_RESP_FILE
            defprob = 0.05
            entry['count'] = 0

        try:
            respdata = shelve.open(respfile)
            if key in respdata:
                entry['responses'].union(set(respdata[key]['responses']))
                entry['probability'] = (probability if probability is not None
                                        else respdata[key]['probability'])
            else:
                entry['probability'] = (probability if probability is not None
                                        else defprob)

            respdata[key] = entry
            exitmsg = ['stored']
        except:
            exitmsg = ["couldn't store that for some reason"]
        finally:
            respdata.close()
        return exitmsg


class StoredResponses(CmdsProvider):
    eventual_resp_file = EVENTUAL_RESP_FILE
    immediate_resp_file = IMMEDIATE_RESP_FILE
    respond_to_public = True
    cmds = {}

    def pre_process(self, command, conn_obj, data):
        try:
            eventual_respdict = shelve.open(self.eventual_resp_file)
            lcmd = command.strip().lower()
            if lcmd in eventual_respdict:
                respitem = eventual_respdict[lcmd]

                respitem['count'] += 1
                eventual_respdict[lcmd] = respitem
        finally:
            eventual_respdict.close()
        return command, data

    def match_command(self, command, conn_obj, data):
        lcmd = command.strip().lower()
        try:
            immediate_respdict = shelve.open(self.immediate_resp_file)
            if lcmd in immediate_respdict:
                resp = immediate_respdict[lcmd]
                if random.random() < resp['probability']:
                    data['response'] = random.choice(list(resp['responses']))
                    immediate_respdict.close()
                    return self.cmd_reply, command, data
        finally:
            immediate_respdict.close()

        try:
            eventual_respdict = shelve.open(self.eventual_resp_file)
            for key, value in eventual_respdict.items():
                if (value['count'] and random.random() < value['probability']
                        and not data['to_me']):
                    value['count'] -= 1
                    data['response'] = random.choice(list(value['responses']))
                    eventual_respdict[key] = value
                    eventual_respdict.close()
                    return self.cmd_reply, command, data
            eventual_respdict.close()
        except:
            pass

        return None, None, data

    def cmd_reply(self, command, data):
        return [data['response']]
