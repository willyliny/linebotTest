from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import *
import config
import line_richmenu_config as richmenu_config


line_bot_api = LineBotApi(config.line_token["Channel_access"])

# 沒用到
def delete_all_richmenu():
	rich_menu_list = line_bot_api.get_rich_menu_list()
	for rich_menu in rich_menu_list:
		line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

# 抓取richmenu_id
def get_richmenu_id(name):
	rich_menu_list = line_bot_api.get_rich_menu_list()
	findid = False
	rich_menu_list = dict((x.name,x.rich_menu_id) for x in rich_menu_list)
	if name in rich_menu_list:
		return rich_menu_list[name]
	else:
		if name in richmenu_config.map_list:
			item = richmenu_config.map_list[name]
			rich_menu_id = line_bot_api.create_rich_menu(rich_menu=item["menu"])
			with open(item["path"], 'rb') as f:
				line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)
			return rich_menu_id
	return None
