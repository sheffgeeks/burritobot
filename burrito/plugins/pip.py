from burrito.cmdsprovider import CmdsProvider
from burrito.utils import reply_to_user

import xmlrpc.client


class Pip(CmdsProvider):

    def __init__(self):
        self.cmds = {
              'pip': {
                  'function': self.get_package,
                  'description': "Get pip package",
                  'aliases': ['pypi', ],
              }
        }

        self.xml_rpc = xmlrpc.client.ServerProxy("http://pypi.python.org/pypi")

    def get_package(self, command, data):
        """Return the package version and url, or alternatives if not found"""
        args = " ".join(command.split(":")[1:])
        response = self.xml_rpc.search({"name": args})

        alts = []
        for item in response:
            if item["name"].lower() == args.lower():
                wanted_data = item
                break
            elif args.lower() in item["name"].lower():
                alts.append(item["name"])
        else:
            if alts:
                reply = "Package {} not found. Alternatives: {}".format(args, " ".join(alts[:10]))
                return reply_to_user(data, reply)
            else:
                return reply_to_user(data, "Package {} not found".format(args))

        response = self.xml_rpc.release_data(wanted_data["name"], wanted_data["version"])

        reply = "{} {}: {}".format(wanted_data["name"],
                               wanted_data["version"],
                               response["home_page"])

        return reply_to_user(data, reply)