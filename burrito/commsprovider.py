#!/usr/bin/env python3

from burrito.mountpoint import PluginMount

class CommsProvider(metaclass=PluginMount):
    """
    Mount point for classes providing the main communication methods.

    This needs to provide:
     * add_cli_args(self, parser) - specifies argparse options
     * setup(self, options) - performs any setup with the options provided
     * run(self) - starts the comms process
    """


if __name__ == '__main__':
    comms = CommsProvider.get_plugins()
    print([c.name for c in comms])

