from irc3.plugins.command import command
import irc3

import xmlrpc.client
import string


@irc3.plugin
class Pip(object):

    def __init__(self, bot):
        self.bot = bot
        self.xml_rpc = xmlrpc.client.ServerProxy("http://pypi.python.org/pypi")

    @command(permission='view', name='pip')
    def pip(self, mask, target, args):
        """Return the package version and url, or alternatives if not found

            %%pip <package>
        """
        reply = self.get_package(mask, target, args)
        if target.is_channel:
            return "{user}: {reply}".format(user=mask.nick, reply=reply)
        return reply

    def get_package(self, mask, target, args):
        package = args.get('<package>')

        allowed_chars = string.ascii_letters + string.digits + "_-."
        for char in package:
            if char not in allowed_chars:
                return 'Invalid name: Cannot contain "{}"'.format(char)

        self.bot.log.info('searching for package {}'.format(package))
        response = self.xml_rpc.search({"name": package})

        alts = []
        for item in response:
            if item["name"].lower() == package.lower():
                wanted_data = item
                break
            elif package.lower() in item["name"].lower():
                alts.append(item["name"])
        else:
            if alts:
                return "Package {} not found. Alternatives: {}".format(package, " ".join(alts[:10]))
            else:
                return "Package {} not found".format(package)

        response = self.xml_rpc.release_data(wanted_data["name"], wanted_data["version"])

        reply = "{} {}: {} {}".format(wanted_data["name"],
                                      wanted_data["version"],
                                      response["summary"],
                                      response["home_page"])

        return reply
