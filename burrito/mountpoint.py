#!/usr/bin/env python3


class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)

    def get_plugins(cls, *args, **kwargs):
        return [p(*args, **kwargs) for p in cls.plugins]


"""
To use, specify mount points as classes:

>>> class EventProvider(metaclass=PluginMount):
        "mount point for events"

along with any documentation and common code for the mount point, then any
code that inherits the mount point is a plugin

>>> class SomeEvent(EventProvider):
        def __init__(self):
            print("initialised")

Then something like the following will get all the plugins and allow you to
work with them:

>>> events = EventProvider.get_plugins()
>>> [e.process() for e in events]
"""
