"""
LINE WEBHOOK For CHATBOT HKATRON 2017 @ THAILAND
Since: 18 Mar. 2017
"""
# pylint: disable=invalid-name

import os
from wit import Wit
from actions import ACTIONS
from flask import Flask, request, abort, g

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

LINE_SECRET = os.environ.get('LINE_SECRET')
LINE_TOKEN = os.environ.get('LINE_TOKEN')
WIT_TOKEN = os.environ.get('WIT_TOKEN')

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_TOKEN)
wit_client = Wit(access_token=WIT_TOKEN, actions=ACTIONS)
parser = WebhookParser(LINE_SECRET)

g._context = {}

@app.route("/line", methods=['POST'])
def callback():
    """
    used for LINE Webhook
    """
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    context = getattr(g, '_context', {})
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        # No response to message from LINE verify webhook
        if event.reply_token == 'f'*32 or event.reply_token == '0'*32:
            continue
        # send to wit.ai
        context = wit_client.run_actions('', event.message.text, context)
        app.logger.info(context)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(context))
        )

    return 'OK'

@app.route("/line/yo")
def hello_word():
    """
    Route for helloworld echo
    """
    app.logger.info('WIT_TOKEN: {0}\nLINE_TOKEN: {1}'.format(WIT_TOKEN, LINE_TOKEN))
    return "Hello world"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
