burritobot
==========

An irc bot that has undisclosed burrito opinions

To install:

```sh
virtualenv burritoenv -p python3
source burritoenv/bin/activate
pip install irc
python setup.py install
```

For development purposes, instead use:

```sh
python setup.py develop
```

To run:

```sh
burritobot --irc-channels "#channel1" "#channel2" --irc-nick mynick
```

The above will connect as mynick on freenode, joining #channel1 and #channel2.

Run:

```sh
burritobot --help
```

to discover any further options.
