from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from pymongo import MongoClient
from linebot.models import *
from flask import Flask, request, abort
import line_richmenu_tools as richmenu_tools
import config
import json

MONGO_URI = "mongodb://36.225.63.171:27017/face_data"
client = MongoClient(MONGO_URI)
db = client['face_data']
collection = db['mydata']

app = Flask(__name__)

#匯入金鑰
line_bot_api = LineBotApi(config.line_token["Channel_access"])
handler = WebhookHandler(config.line_token["Channel_secret"])

DATA_PATH = '../face_code/data/output.json'

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

@app.route("/people", methods=['GET'])
def people():
    # 从 MongoDB 中获取最新一条数据
    latest_data = collection.find().sort([('_id', -1)]).limit(1).next()

    if latest_data:
        image_message = ImageSendMessage(
                original_content_url=latest_data["img_link"],
                preview_image_url=latest_data["img_link"]
            )
        line_bot_api.push_message('Ucd05e33d7f362018934e180787b5c837', image_message)
        return "我呼叫到 /people 拉"
    else:
        return "not found data"


#有使用者加入時會執行
@handler.add(FollowEvent)
def handle_follow(event):
    rich_menu_id = richmenu_tools.get_richmenu_id("main_menu")
    line_bot_api.link_rich_menu_to_user(event.source.user_id, rich_menu_id)
    message = TextSendMessage(text = "歡迎加入人流監控測試系統")
    line_bot_api.reply_message(event.reply_token, message)

#有使用者留言時會執行
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

#Rich Menu被點擊時會執行對應功能
@handler.add(PostbackEvent)
def handle_postback(event):
    command = event.postback.data

    # 从 MongoDB 中获取最新一条数据
    latest_data = collection.find().sort([('_id', -1)]).limit(1).next()


    # 點擊即時人流
    if command == 'people_number':
        message = TextSendMessage(text='目前場地人數 : '+str(latest_data["people_counter"]))
        line_bot_api.reply_message(event.reply_token, message)

    # 點擊最新通報
    elif command == 'news_alert':       
        message = TextSendMessage(text = "上次違規影像為: \n" + latest_data["img_link"])
        
        line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)