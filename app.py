from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('6ol/TkzOsx2Ej9mikY8+FU6SegSuiLpMWg8v9aLR+VJ/ERdnRFmEYoLQ2QCXZQb34Mhr5saLpkSH+5FeyQa3zaDekwISNXef8rq8FVSyuSAiSVFiQakv9u9PM6qq3dMrZ7YxbsxB2pyItBZaISwdRgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e73f4ba68c0127b885304278fe5fd152')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

def Reply(event):
    return line_bot_api.reply_message(event.reply_token,
        TemplateSendMessage(
            alt_text='替代文字',
            template=ButtonsTemplate(
                thumbnail_image_url='圖案路徑.jpg',
                title='標題',
                text='內容',
                actions=[
                    PostbackTemplateAction(
                    label='按鈕文字',
                    text='發話文字',
                    data='夾帶資料'
                    ),
                    MessageTemplateAction(
                        label='按鈕文字',
                        text='發話文字'
                    ),
                    URITemplateAction(
                        label='按鈕文字',
                        uri='網址'
                    )
                ]
            )
        )
    )

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Reply(event)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)