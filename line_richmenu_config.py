from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import *
import datetime

main_menu = RichMenu(
	size=RichMenuSize(width=1200, height=405),
	selected=True,  #是否預設跳出
	name="no_login",
	chat_bar_text="工具列",
	areas=[
		RichMenuArea(
			bounds = RichMenuBounds(x=0   , y=0, width=600 , height=405),
			action = PostbackAction(data = 'people_number')
		),
		RichMenuArea(
			bounds = RichMenuBounds(x=600   , y=0, width=600 , height=405),
			action = PostbackAction(data ='news_alert')
		),
	]
)


map_list = {
	'main_menu' : {
				"menu" : main_menu,
				"path" : "richmenu/main_menu.png"
			}
}


