# burritobot

An irc bot that has undisclosed burrito opinions

## Installing

### Option 1: Manually in a virtualenv:

This method assumes you already have python 3 and python-virtualenv installed
appropriately.

Create a virtualenv and activate it:
```sh
virtualenv burritoenv -p python3
source burritoenv/bin/activate
```

and install:
```sh
pip install irc
python setup.py install
```

### Option 2: Using Vagrant (>= 1.3.0):

This method assumes a fairly recent version of Vagrant is already installed
(see the [vagrant website](http://www.vagrantup.com).)

The following downloads the base virtualbox VM (first time only), starts it up
and installs:

```sh
vagrant up
```

To run (see below) you will also need to access the VM:

```sh
vagrant ssh
```

## Running

If are not already in the activated burritoenv environment:
```sh
source burritoenv/bin/activate
```

To run:
```sh
burritobot --irc-channels "#channel1" "#channel2" --irc-nick mynick
```

The above will connect as mynick on freenode, joining #channel1 and #channel2.


To discover further options, run

```sh
burritobot --help
```
