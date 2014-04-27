# How to Contribute

## PySheff April 2014

The current plan for contributing during the Python Sheffield event is to
entrust all those who attend with the ability to commit directly to the
repository.

To get started you will need a GitHub account (if you do not already have an
account [signup here](https://github.com/signup/free).

## Installing in development mode

Two alternative methods of installing are documented here.

The vagrant variant requires the download of vagrant itself along with a base
VM which, on a limited network connection, might seem a bit excessive. These
instructions also assume that you will be able to ssh in to the VM to start
the bot.

The alternative virtualenv method does require a bit extra knowledge for your
operating system as you will need to have Python 3.x, virtualenv and pip
installed.

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
python setup.py develop
```

### Option 2: Using Vagrant (>= 1.3.0):

This method assumes a fairly recent version of Vagrant is already installed
(see the [vagrant website](http://www.vagrantup.com).)

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
burritobot --irc-channels burritobottest --irc-nick myburritonick --debug
```

The above will connect as mynick on freenode, and will join #burritotest. You
may prefer to join a different channel if you wish to keep your changes a
surprise. You will almost certainly need to choose a unique nickname for the
bot to avoid naming conflicts.

## Coding Standards

[PEP-8](https://www.python.org/dev/peps/pep-0008/)

## Notes for Making Plugins

Currently the process is a little clunky but should not be hugely difficult.

* Create a new file with your plugin code in the plugins directory
* Your plugin at the moment is likely to be a "CmdsProvider" so you should be
  importing and the reply_to_user helper function:
  ```python
  from burrito.cmdsprovider import CmdsProvider
  from burrito.utils import reply_to_user
  ```
* Create a python class that inherits CmdsProvider
  ```python
  class MyCmd(CmdsProvider):
      [...]
  ```
* Write one or more methods that represent commands that will be called. To
  respond to a user they can use the reply_to_user function:
  ```python
      def my_cmd(self, command, data):
          [...]
          return reply_to_user(data, reply)
  ```
* In the __init__ method store a dictionary to map commands to trigger your
  method:
  ```python
      def __init__(self):
          self.cmds = {
              'mycmd': {
                  'function': self.my_cmd,
                  'description': "what mycmd does",
                  'aliases': ['altmycmd', ],
              }
          }
  ```
  Note that if there is no description, or there is a 'nolist' defined for the
  command - the commands plugin will not currently list the command.
  See also [default command handling notes](#command-name-notes))
* Finally in the __init__.py file in the plugins directory, add the name of
  the new module to the __all__ list.

If you wish to process data without having to be triggered by the bot being
addressed, you can add a pre_process method to your class:
```python
    def pre_process(self, command, conn_obj, data):
        # do your processing
        return command, data
```

### <a name="command-name-notes"></a>Notes on default command name handling:

The default command handling attempts to help users so that they can call your
command in a number of forms. Specifying aliases extends this for additional
ways of helping that are not predicted. For example if we have:
```python
class StatusCmd(CmdsProvider):
    def __init__(self):
        self.cmds = {
            'statusforall': {
                'function': self.cmd_getallstatus,
                'aliases': ['whatiseveryonedoing', 'whatseveryonedoing',
                            'whatiseverybodydoing', 'whatseverybodydoing', ],
            }
        }
```
the StatusCmd.cmd_getallstatus method will be called in response to (amongst
many similar alternatives):
* <botname>: statusforall
* <botname>: status for all
* <botname>: what's everyone doing?
* <botname>: w hats every body'd oing!

All this also works on the assumption that the command name is effectively the
text between the colon after the nickname of the bot and either the end of the
line of input or the next colon. Arguments to the command are therefore
expected after the colon following the trigger.

If you want to implement triggers in a different way, you can override the
match_command method for your class.

