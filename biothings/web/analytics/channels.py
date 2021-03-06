import json

import certifi
from biothings.web.analytics.events import *
from tornado.httpclient import HTTPRequest


class Channel:

    def handles(self, event):
        raise NotImplementedError()

    def send(self, event):
        raise NotImplementedError()


class SlackChannel(Channel):

    def __init__(self, hook_urls):
        self.hooks = hook_urls

    def handles(self, event):
        return isinstance(event, Message)

    def send(self, message):
        for url in self.hooks:
            yield HTTPRequest(
                url=url,
                method='POST',
                headers={'content-type': 'application/json'},
                body=json.dumps(message.to_slack_payload()),
                ca_certs=certifi.where()  # for Windows compatibility
            )

# Measurement Protocol (Universal Analytics)
# https://developers.google.com/analytics/devguides/collection/protocol/v1/devguide

class GAChannel(Channel):

    def __init__(self, tracking_id, uid_version=1):
        self.tracking_id = tracking_id
        self.uid_version = uid_version

    def handles(self, event):
        return isinstance(event, Event)

    def send(self, payload):
        yield HTTPRequest(
            'http://www.google-analytics.com/batch', method='POST',
            body='\n'.join(payload.to_GA_payload(self.tracking_id, self.uid_version))
        )
