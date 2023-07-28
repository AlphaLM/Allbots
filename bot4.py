import telebot
from telebot.types import *
import pyshorteners
from pymongo import MongoClient

API_TOKEN = "5647131346:AAGTnRcX1TZw6t5GIC0c71zIX0jeKHpS1ks"

admin= [1365625365]

client = MongoClient("mongodb+srv://really651:gSPMW6u9WuStXIwD@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")


db = client["Shortner"]
collection = db["shorter"]


bot = telebot.TeleBot(API_TOKEN, parse_mode = "html")


@bot.inline_handler(lambda query: True)
def a(message):
	if len(message.query) ==0:
		r8 = InlineQueryResultArticle("99", "Enter a <<url>> to short!", InputTextMessageContent("Enter the url to be shorted▼"), description ="Enter <<URL>>", thumb_url="https://t.me/proversion100/25")
		bot.answer_inline_query(message.id, [r8])
		return
	else:
		long_url = message.query
		if not '.' in long_url:
			return
		x = pyshorteners.Shortener()
		short_url = x.tinyurl.short(long_url)
		r9 = InlineQueryResultArticle("1", "Click Here!", InputTextMessageContent(short_url), description =short_url, thumb_url ="https://t.me/proversion100/25")
		bot.answer_inline_query(message.id, [r9])


az = InlineKeyboardMarkup()
a01 = InlineKeyboardButton(text ="🕹Join My Updates🕹", url="t.me/mt_projectz")
a02 = InlineKeyboardButton(text ="Inline Here✨", switch_inline_query_current_chat="https://t.me/MT_Projectz")
az.add(a02)
az.add(a01)

btn = InlineKeyboardMarkup()
b = InlineKeyboardButton(text ="JOIN🗃", url="t.me/mt_projectz")
btn.add(b)

@bot.message_handler(commands = ["start"])
def send_messag(message):
	user = collection.find_one({"user_id": message.chat.id})
	if user:
		bot.send_message(message.chat.id, f"👋Hey {message.chat.first_name},\n\nThis bot can short long links to just simple links🤖\nJust send a link or Use Inline🔄", reply_markup = az)
	else:
		collection.insert_one({"user_id": message.chat.id})
		bot.send_message(message.chat.id, f"👋Hey {message.chat.first_name},\n\nThis bot can short long links to just simple links🤖\nJust send a link or Use Inline🔄", reply_markup = az)

@bot.message_handler(commands = ["stats"])
def check_stats(message):
	if message.chat.id in admin:
		users = list(collection.find())
		bot.send_message(message.chat.id, f"Total Users: {len(users)}")

btn = InlineKeyboardMarkup()
b = InlineKeyboardButton(text ="JOIN🗃", url="t.me/mt_projectz")
btn.add(b)

@bot.message_handler(func = lambda message: True)
def short(message):
	if bot.get_chat_member("@mt_projectz", message.chat.id).status == "left":
		return bot.send_message(message.chat.id, "⚠️Before using this bot you must be a member of our channel🔔\n@MT_Projectz", reply_markup = btn)
	else:
		pass
	long_url = message.text
	if not '.' in long_url:
		return
	try:
		x = pyshorteners.Shortener()
		short_url = x.tinyurl.short(long_url)
		key = InlineKeyboardMarkup()
		k = InlineKeyboardButton(text =" 📎Share Your Link⤵️", url=f"https://t.me/share/url?url={short_url}")
		key.add(k)
		bot.reply_to(message, f"<i>📎Your short link is {short_url}</i>", disable_web_page_preview = True, reply_markup = key)
	except:
		pass

def start_bot4():
  print("Successful")
  bot.infinity_polling() 