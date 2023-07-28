import telebot
from telebot.types import *
import PyPDF2
import os
import tempfile
from fpdf import FPDF
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://really651:gSPMW6u9WuStXIwD@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["Text2pdf"]
collection = db["pdfbot"]

bot =  telebot.TeleBot("6385541681:AAHqjFy3uIb8SlYYNe1GczF-jjTbN4ahVP0", parse_mode="html")

keyboard = InlineKeyboardMarkup()
k1 = InlineKeyboardButton(text ="💼JOIN NOW💼", url="t.me/mt_projectz")
keyboard.add(k1)

def text_to_pdf(text, output_path, message):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.cell(200, 10, txt = text, ln = 1,)
    pdf.output(output_path)

def convert_pdf_to_text(pdf_path, message):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    pdf_file.close()
    chunks = [text[i:i+4096] for i in range(0, len(text), 4096)]
    for chunk in chunks:
    	return bot.send_message(message.chat.id, chunk)

btn = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton("🕹Join My Updates🕹", url="t.me/mt_projectz")
btn.add(btn1)

@bot.message_handler(commands =["start"])
def start(message):
	user = collection.find_one({"user_id": message.from_user.id})
	if user:
		bot.reply_to(message, "Hey {}👋,\n\nThis bot can help you to change Text to PDF & vice versa:)🤗\n\n■Just Send Text Or Upload PDF...✨".format(message.from_user.first_name), reply_markup=btn)
	else:
		collection.insert_one({"user_id": message.from_user.id, "first_name": message.from_user.first_name})
		bot.reply_to(message, "Hey {}👋,\n\nThis bot can help you to change Text to PDF & vice versa:)🤗\n\n■Just Send Text Or Upload PDF...✨".format(message.from_user.first_name), reply_markup=btn)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if bot.get_chat_member("@mt_projectz", message.from_user.id).status == "left":
        return bot.send_message(message.chat.id, "⚠️ {} before using this bot, you have to Join projects channel! ■ @MT_Projectz".format(message.from_user.first_name), reply_markup=keyboard)
    else:
        bot.send_chat_action(message.chat.id, "upload_document")
        output_file_path = "Output.pdf"
        text_to_pdf(text=message.text, output_path=output_file_path, message=message)
        with open(output_file_path, "rb") as file:
            try:
                bot.send_document(message.chat.id, file, caption="<b>If You Wanna Change This Filename, Use @Files_Renamer_v4Robot</b>")
                os.remove(output_file_path)  
            except Exception as e:
                bot.reply_to(message, f'Oops, something went wrong. Error: {e}')

@bot.message_handler(content_types=['document'])
def handle_pdf_document(message):
    if bot.get_chat_member("@mt_projectz", message.from_user.id).status == "left":
        return bot.send_message(message.chat.id, "⚠️ {} before using this bot, you have to Join projects channel! ■ @MT_Projectz".format(message.from_user.first_name), reply_markup=keyboard)
    else:
        try:
            chat_id = message.chat.id

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            if message.document.file_name.endswith('.pdf'):
                temp = tempfile.NamedTemporaryFile(delete=False)
                temp.write(downloaded_file)
                temp.close()
                text = convert_pdf_to_text(temp.name, message)
                os.unlink(temp.name)              
        except Exception as e:
            bot.reply_to(message, f'Oops, something went wrong. Error: {e}\nNB: Only PDF format is supported')

def start_bot1():
  print("bot1 is Ready!")
  bot.infinity_polling()