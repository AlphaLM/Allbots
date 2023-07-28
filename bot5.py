import requests
import random
from mtranslate import translate
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup 
from pymongo import MongoClient

bot = telebot.TeleBot("6177434340:AAG7KeRx1uE2RiuIqPV0FD_H-jMWTuTRe1w", parse_mode ="html")

client = MongoClient("mongodb+srv://really651:gSPMW6u9WuStXIwD@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["Qoutesdb"]
collection = db["qoutes"]

dasheng = InlineKeyboardMarkup()
a1 = InlineKeyboardButton(text ="🔄Random", callback_data ="enrandom")
a2 = InlineKeyboardButton(text ="ℹ️About Us", callback_data ="about")
a3 = InlineKeyboardButton(text ="🌍Language", callback_data ="lang")
dasheng.add(a1)
dasheng.add(a2,a3)

dashom = InlineKeyboardMarkup()
om1 = InlineKeyboardButton(text ="🔄Random", callback_data ="omrandom")
om2 = InlineKeyboardButton(text ="ℹ️About Us", callback_data ="about")
om3 = InlineKeyboardButton(text ="🌍Language", callback_data ="lang")
dashom.add(om1)
dashom.add(om2,om3)

dasham = InlineKeyboardMarkup()
am1 = InlineKeyboardButton(text ="🔄Random", callback_data ="amrandom")
am2 = InlineKeyboardButton(text ="ℹ️About Us", callback_data ="about")
am3 = InlineKeyboardButton(text ="🌍Language", callback_data ="lang")
dasham.add(am1)
dasham.add(am2,am3)

@bot.message_handler(commands =["start"])
def start(message):
	id = message.from_user.id
	user = collection.find_one({"user_id": id})
	
	if user:
		if user["lang"] == "en":
			bot.send_message(message.chat.id, "Hey {} 👋\n\nWelcome to Quotes Bot! This bot can give you Quotes written by a lot of persons:)\nℹ️You can change Language to your Language!".format(message.from_user.first_name), reply_markup =dasheng)
		if user["lang"] =="om":
			bot.send_message(message.chat.id, "Hey {} 👋\n\nWelcome to Quotes Bot! This bot can give you Quotes written by a lot of persons:)\nℹ️You can change Language to your Language!".format(message.from_user.first_name), reply_markup =dashom)
		if user["lang"] =="am":
			bot.send_message(message.chat.id, "Hey {} 👋\n\nWelcome to Quotes Bot! This bot can give you Quotes written by a lot of persons:)\nℹ️You can change Language to your Language!".format(message.from_user.first_name), reply_markup =dasham)
	else:
		key = InlineKeyboardMarkup(row_width = 1)
		k1 = InlineKeyboardButton(text ="Oromic", callback_data ="om")
		k2 = InlineKeyboardButton(text ="Amharic", callback_data ="am")
		k3 = InlineKeyboardButton(text ="English", callback_data ="en")
		key.add(k1,k2,k3)
		bot.send_message(message.chat.id, "🌍Choose your Language:\nNB: You can change this in settings later✍️", reply_markup = key)		

lang = InlineKeyboardMarkup()
orom = InlineKeyboardButton(text ="Oromic", callback_data ="oromic")
amhr = InlineKeyboardButton(text ="Amharic", callback_data ="amharic")
engl = InlineKeyboardButton(text ="English", callback_data ="english")
lang.add(orom, amhr, engl)

@bot.callback_query_handler(func = lambda callback: True)
def choose_lang(callback):
	print(callback.data)
	id = callback.from_user.id
	response = requests.get("https://type.fit/api/quotes")
	quotes = response.json()
	random_quote = random.choice(quotes)
	text = random_quote['text']
	author = random_quote['author']
	data = callback.data 
	if data =="om":	
		collection.insert_one({"user_id": id, "lang": "om"})
		bot.send_message(callback.message.chat.id, "Hey {} 👋\n\nWelcome to Quotes Bot! This bot can give you Quotes written by a lot of persons:)\nℹ️You can change Language to your Language!".format(callback.from_user.first_name), reply_markup = dashom)
	if data =="am":
		collection.insert_one({"user_id": id, "lang": "am"})
		bot.send_message(callback.message.chat.id, "Hey {} 👋\n\nWelcome to Quotes Bot! This bot can give you Quotes written by a lot of persons:)\nℹ️You can change Language to your Language!".format(callback.from_user.first_name), reply_markup = dasham)
	if data =="en":
		collection.insert_one({"user_id": id, "lang": "en"})
		bot.send_message(callback.message.chat.id, "Hey {} 👋\n\nWelcome to Quotes Bot! This bot can give you Quotes written by a lot of persons:)\nℹ️You can change Language to your Language!".format(callback.from_user.first_name), reply_markup = dasheng)
	if data =="oromic":
		collection.update_one({'user_id': id}, {'$set': {'lang': "om"}})
		bot.delete_message(callback.message.chat.id, callback.message.message_id)
		bot.send_message(callback.message.chat.id, "✅Language has been set to Oromic!")
		bot.send_message(callback.message.chat.id, "Hey {} 👋\n\nWelcome to Quotes Bot! This bot can give you Quotes written by a lot of persons:)\nℹ️You can change Language to your Language!".format(callback.from_user.first_name), reply_markup = dashom)
	if data =="amharic":
		collection.update_one({'user_id': id}, {'$set': {'lang': "am"}})
		bot.delete_message(callback.message.chat.id, callback.message.message_id)
		bot.send_message(callback.message.chat.id, "✅Language has been set to Amharic!")
		bot.send_message(callback.message.chat.id, "Hey {} 👋\n\nWelcome to Quotes Bot! This bot can give you Quotes written by a lot of persons:)\nℹ️You can change Language to your Language!".format(callback.from_user.first_name), reply_markup = dasham)
	if data =="english":
		collection.update_one({'user_id': id}, {'$set': {'lang': "en"}})
		bot.delete_message(callback.message.chat.id, callback.message.message_id)
		bot.send_message(callback.message.chat.id, "✅Language has been set to English!")
		bot.send_message(callback.message.chat.id, "Hey {} 👋\n\nWelcome to Quotes Bot! This bot can give you Quotes written by a lot of persons!\nℹ️You can change Language to your Language!".format(callback.from_user.first_name), reply_markup = dasheng)
	if data=="lang":
		bot.delete_message(callback.message.chat.id, callback.message.message_id)
		bot.send_message(callback.message.chat.id, "Choose your language:)", reply_markup = lang)		
	if data =="omrandom":
		orotrans = translate(text, "om")
		bot.delete_message(callback.message.chat.id, callback.message.message_id)
		if author == None:
			textom=f"""<b>{orotrans}</b>\n\n✍️ Unknown"""
			bot.send_message(callback.message.chat.id, textom, reply_markup = dashom)
		else:
			textom=f"""<b>{orotrans}</b>\n\n✍️ {author}"""
			bot.send_message(callback.message.chat.id, textom, reply_markup = dashom)
	if data =="amrandom":
		amtrans = translate(text, "am")
		bot.delete_message(callback.message.chat.id, callback.message.message_id)
		if author == None:
			textam=f"""<b>{amtrans}</b>\n\n✍️ Unknown"""
			bot.send_message(callback.message.chat.id, textam, reply_markup = dasham)
		else:
			textam=f"""<b>{amtrans}</b>\n\n✍️ {author}"""
			bot.send_message(callback.message.chat.id, textam, reply_markup = dasham)
	if data =="enrandom":
		bot.delete_message(callback.message.chat.id, callback.message.message_id)
		if author == None:
			texten=f"""<b>{text}</b>\n\n✍️ Unknown"""
			bot.send_message(callback.message.chat.id, texten, reply_markup = dasheng)
		else:
			texten=f"""<b>{text}</b>\n\n✍️ {author}"""
			bot.send_message(callback.message.chat.id, texten, reply_markup = dasheng)
	if data =="about":
		bot.send_message(callback.message.chat.id, "<b>📢Join @MT_PROJECTZ for my Updates:)</b>")

def start_bot5():
  print("Successful")
  bot.infinity_polling()