from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('aYwj4REbu5yC68RSirrBDQVxgXHsMeBU6FHWrv4UPgXf92aYdiexKFCkHPphZtw0VMeJizqzmWRVV55EpoF2Ivj3ItWaj3P0Qzhh7ChOh1g9IVGil0qbW290QggvJs0TrRoLQIAb0+yqIqakSXvjCgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b268543f01c5d4c5b88ccfb0d21c6580')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '我看不懂你說甚麼'

    if msg == 'hi':
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是周志鵬'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()