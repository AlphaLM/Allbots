import telebot
from telebot.types import *
import requests
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://really651:gSPMW6u9WuStXIwD@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["img2txt"]
collection = db["img2txtbot"]

bot = telebot.TeleBot('6067426588:AAGtmW1FSv52pvylsUXHAHqqLnp32YSDnLA')

keyboard = InlineKeyboardMarkup()
key = InlineKeyboardButton(text ="🕹Join My Updates🕹", url="t.me/mt_projectz")
keyboard.add(key)

@bot.message_handler(commands =["start"])
def start(message):	
	welcomemsg = f"Hey {message.from_user.first_name}👋,\n\nThis bot can help you to extract texts from your images/photos easily🕹\n🚀Just send me your image/photo..."
	user = collection.find_one({"user_id": message.chat.id})
	if user:
		bot.send_message(message.chat.id, welcomemsg, reply_markup = keyboard)
	else:
		collection.insert_one({"user_id": message.chat.id})
		bot.send_message(message.chat.id, welcomemsg, reply_markup = keyboard)

@bot.message_handler(content_types=['photo'], chat_types=["private"])
def handle_photo(message):
    if bot.get_chat_member("@mt_projectz", message.chat.id).status == "left":
    	return bot.send_message(message.chat.id, f"⚠️Dear {message.from_user.first_name} In order to use this bot you must be a member of our channel\n@MT_Projectz", reply_markup=keyboard)
    else:
    	pass
    a = bot.reply_to(message," 🚀Extracting your text....")
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)    
    api_key = 'K81164834388957'
    url = 'https://api.ocr.space/parse/image'
    payload = {
        'apikey': api_key,
        'language': 'eng',
        'isOverlayRequired': False
    }
    files = {
        'filename': ('image.jpg', downloaded_file, 'image/jpeg')
    }
    response = requests.post(url, data=payload, files=files)
    if response.status_code == 200:
        response_data = response.json()
        if response_data['IsErroredOnProcessing']:
            error_message = response_data['ErrorMessage']
            bot.send_message(message.chat.id, f'Error: {error_message}\nReport to @MT_ProjectzChat')
        else:
            extracted_text = response_data['ParsedResults'][0]['ParsedText']
            bot.delete_message(message.chat.id, a.id)
            bot.send_message(message.chat.id, f"Here is the text:\n\n<code>{extracted_text}</code>", parse_mode ="html")
    else:
        bot.send_message(message.chat.id, 'Error: Report to @MT_ProjectzChat')

def start_bot2():
  print("bot2 is ready!")
  bot.infinity_polling()