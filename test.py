"""
Interactive test for WIT
"""
# pylint: disable=invalid-name

import os
from wit import Wit

WIT_TOKEN = os.environ.get('WIT_TOKEN')

def send(_, response):
    """
    hook response from wit.ai to line
    """
    print('response: {0}'.format(response['text']))

ACTIONS = {
    'send': send
}

print("TOKEN: {0}".format(WIT_TOKEN))

client = Wit(access_token=WIT_TOKEN, actions=ACTIONS)
client.interactive()
