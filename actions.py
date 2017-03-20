"""
WIT.AI Actions
"""
def send(_, response):
    """
    Simple logging response
    """
    print(response['text'])

ACTIONS = {
    'send': send
}
