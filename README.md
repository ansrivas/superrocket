# superrocket


Short Description:
---
A supervisord process notification for rocketchat.

This project has been highly inspired from the [superslacker](https://github.com/MTSolutions/superslacker) project.

## Usage:
To use it with supervisor put this as a plugin in your `supervisor.conf`

```
[eventlistener:superslacker]
command=superslacker --webhook="your-complete-rocketchat-webhook" --channel="#notifications" --hostname="HOST"
events=PROCESS_STATE,TICK_60
```


## Options:
```
usage: superrocket [-h] -c CHANNEL -w WEBHOOK [-a ATTACHMENT] [-n HOSTNAME]
                   [-b BOTNAME] [-k]

Send messages from supervisor state changes, to RocketChat

optional arguments:
  -h, --help            show this help message and exit
  -c CHANNEL, --channel CHANNEL
                        RocketChat channel to post message to
  -w WEBHOOK, --webhook WEBHOOK
                        RocketChat WebHook URL
  -a ATTACHMENT, --attachment ATTACHMENT
                        RocketChat attachment text
  -n HOSTNAME, --hostname HOSTNAME
                        System Hostname
  -b BOTNAME, --botname BOTNAME
                        Default username for the bot
  -k, --insecure        Skip RocketChat server certificate verification
```


## Current Stable Version
```
0.1.0
```
## Installation
### via pip
```
pip install superrocket
```
### Development Installation
* Clone the project.
* Install in Anaconda3 environment
* This command creates a python environment and then activates it.
```
$ make recreate_pyenv && chmod +x activate-env.sh && . activate-env.sh
```
* Now install the application in editable mode and you are ready to start development
```
$ pip install -e .
```

## Test
To run the tests:
```
make test
```

## Examples
```
$ python examples/simple.py
```
## License
See the LICENSE and Copyright.txt files.
