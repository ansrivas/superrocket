# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Standalone api to be used as a standalone library to be used to send notifications."""

import socket
import requests


class Api(object):
    """Standalone API class to be called from an app to send notifs/messages."""

    def __init__(self, channel, webhook, **kwargs):
        """Initialize the SuperRocket.Api object.

        Args:
            channel (str) : A given RocketChat channel, for eg. "#general"
            webhook (str) : A complete RocketChat webhook url
            hostname (str): A hostname to represent where the message is being sent from
            botname (str) : Readable botname for this bot, defaults to superrocket
            emoji (str)   : Default emoji to be published with this message
        """
        self.channel = channel
        self.webhook = webhook
        self.hostname = kwargs.get('hostname', socket.gethostname())
        self.botname = kwargs.get('botname', "superrocket")
        self.attachment = kwargs.get('attachment', None)
        self.emoji = kwargs.get('emoji', ':rocket:')

    def send(self, msg, verify=True):
        """Send a given message to rocketchat webhook.

        Args:
            msg (str) : Message to be published on the webhook. This could be a markdown as well.
            verify (bool) : requests verify parameter to verify server certificates
        """
        payload = {
            'channel': self.channel,
            'text': msg,
            'username': self.botname,
            'emoji': self.emoji,
            'attachments': [{"text": self.attachment, "color": "#ff0000"}],
        }
        self.__post_message(url=self.webhook, data=payload, verify=verify)

    def __post_message(self, url, data, verify):
        """Send a post request to a given webhook url."""
        with requests.Session() as sess:
            sess.post(url=url, data=data, verify=verify)
