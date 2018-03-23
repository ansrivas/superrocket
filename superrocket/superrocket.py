# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module responsible for supervisor process monitoring."""

import os
import sys
import socket
import requests
import argparse
from supervisor import childutils
from superlance.process_state_monitor import ProcessStateMonitor


class SuperRocket(ProcessStateMonitor):
    """SuperRocket class is responsible for sending rocket.chat webhook messages.

    In case of process status changes SuperRocket sends out an post message to a webhook on rocket.chat
    """

    process_state_events = ['PROCESS_STATE_FATAL', 'PROCESS_STATE_RUNNING',
                            'PROCESS_STATE_EXITED', 'PROCESS_STATE_STOPPED',
                            'SUPERVISOR_STATE_CHANGE']

    def __init__(self, **kwargs):
        """Initialize SuperRocket class instance."""
        ProcessStateMonitor.__init__(self, **kwargs)
        self.channel = kwargs.get('channel')
        self.hostname = kwargs.get('hostname')
        self.botname = kwargs.get('botname')
        self.webhook = kwargs.get('webhook')
        self.attachment = kwargs.get('attachment', None)
        self.insecure = kwargs.get('insecure')

    @classmethod
    def __setup_args(cls):
        """Setup args to accept all the command line entries."""
        parser = argparse.ArgumentParser(description='Send messages from supervisor state changes, to RocketChat')

        parser.add_argument("-c", "--channel", required=True, help="RocketChat channel to post message to")
        parser.add_argument("-w", "--webhook", required=True, help="RocketChat WebHook URL")
        parser.add_argument("-a", "--attachment", help="RocketChat attachment text")
        parser.add_argument("-n", "--hostname", default=socket.gethostname(), help="System Hostname")
        parser.add_argument("-b", "--botname", default="superrocket", help="Default username for the bot")
        parser.add_argument("-k", "--insecure", action="store_true", default=False,
                            help="Skip RocketChat server certificate verification")

        return parser

    @classmethod
    def from_cmd_args(cls):
        """Create an instance of SuperRocket from command line args."""
        args = cls.__setup_args().parse_args()
        options = {key: value for (key, value) in args._get_kwargs()}
        if 'SUPERVISOR_SERVER_URL' not in os.environ:
            sys.stderr.write('Must run as a supervisor event listener\n')
            sys.exit(1)
        return cls(**options)

    def get_emoji(self, eventname):
        """Get emojis based on type of message."""
        emo_keys = {
            "EXITED": ":sob:",
            "STOPPED": ":sob:",
            "FATAL": ":sob:",
            "RUNNING": ":clap:",
            "DEFAULT": ":smile:"
        }
        for key in emo_keys:
            if key in eventname:
                return emo_keys[key]
        return emo_keys["DEFAULT"]

    def get_process_state_change_msg(self, headers, payload):
        """."""
        pheaders, pdata = childutils.eventdata(payload + '\n')
        to_state = headers['eventname']
        emoji = self.get_emoji(to_state)
        msg = ('```Host      : [{0}]\nProcess   : {processname}\nGroupname : {groupname}\nStatus    : '
               '{from_state} => {to_state}``` {emoji}'.format(self.hostname,
                                                              to_state=headers['eventname'],
                                                              emoji=emoji, **pheaders))
        return msg

    def send_batch_notification(self):
        """."""
        message = self.get_batch_message()
        if message:
            self.send_message(message)

    def get_batch_message(self):
        """."""
        return {
            'webhook': self.webhook,
            'channel': self.channel,
            'attachment': self.attachment,
            'insecure': self.insecure,
            'messages': self.batchmsgs,
        }

    def post_message(self, url, data, verify):
        """Send a post request to a given webhook url."""
        with requests.Session() as sess:
            sess.post(url=url, data=data, verify=verify)

    def send_message(self, message):
        """."""
        for msg in message['messages']:
            payload = {
                'channel': message['channel'],
                'text': msg,
                'username': self.botname,
                'emoji': ':sos:',
                'attachments': [{"text": message['attachment'], "color": "#ff0000"}],
            }
            # 'attachments': [{"text": message['attachment'], "color": "#ff0000"}],
            self.post_message(url=message['webhook'], data=payload, verify=False if message['insecure'] else True)
            self.write_stderr("Sent notification over webhook.")


def main():
    """Entry point of the superrocket program."""
    superrocket = SuperRocket.from_cmd_args()
    superrocket.run()


if __name__ == '__main__':
    main()
