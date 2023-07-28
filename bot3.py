import pyrogram	
from pyrogram import Client, filters, idle
from pyrogram.types import *
from pyrogram import enums
import pymongo
from pymongo import MongoClient


client = MongoClient("mongodb+srv://really651:gSPMW6u9WuStXIwD@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["saverbot"]
collection = db["saver"]

app = Client(
"msgsaverbot",
api_id = 11855414,
api_hash = "71449899c824b5bc9a91d8a52b20c5f3",
bot_token = "6207245164:AAHpT8kxfAhbOTUzpav-nJZZdCG8sMPwknE"
)

key = InlineKeyboardMarkup([
[InlineKeyboardButton(text ="🕹My Updates Channel🕹", url="t.me/mt_projectz")]
])


@app.on_inline_query()
async def inline(c , q):
    query = q.query 
    sp = query.split("/")
    mid = sp[-1]
    chan = sp[-2]
    print (query , chan , mid)  
    a = await app.get_messages(chan , int(mid))
    if a.photo:
        await q.answer( results = [
        ( InlineQueryResultCachedPhoto(
        photo_file_id=a.photo.file_id,
        title = "Restricted Content",
        description ="Downloading",
        caption = a.caption, 
    reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
    "Join Us🤗", url="https://t.me/mt_projectz")]])
    ))])
    
    if a.document:				
        await q.answer( results = [
        ( InlineQueryResultCachedDocument(
        document_file_id=a.document.file_id,
        title = "Restricted Content",
        description ="Downloading",
        caption = a.caption, 
    reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
    "Join Us🤗", url="https://t.me/mt_projectz")]])
    ))])
		
    if a.video:						
        await q.answer( results = [
        ( InlineQueryResultCachedVideo(
        video_file_id = a.video.file_id,
        title = "Restricted Content",
        description ="Downloading",
        caption = a.caption, 
    reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
    "Join Us🤗", url="https://t.me/mt_projectz")]])
    ))])
    if a.text:
        await q.answer( results = [ ( InlineQueryResultArticle(
        title = " Restricted content ",
        description ="text message ",
        input_message_content = InputTextMessageContent(a.text) ,
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Join us🤗", url="https://t.me/mt_projectz")]])
		    ))])
    if a.audio:
        await q.answer( results = [
        ( InlineQueryResultCachedAudio(
        audio_file_id=a.audio.file_id,
        title = "Restricted Content",
        description ="Downloading",
        caption = a.caption, 
    reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
    "Join Us🤗", url="https://t.me/mt_projectz")]])
    ))])
    if a.voice:
        await q.answer( results = [
        ( InlineQueryResultCachedVoice(
        voice_file_id=a.voice.file_id,
        title = "Restricted Content",
        caption = a.caption, 
    reply_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(
    "Join Us🤗", url="https://t.me/mt_projectz")]])
    ))])
    else :
        await q.answer( results = [ ( InlineQueryResultArticle(
        title = "Link Required ",
        description ="Pls provide public channel or group link",
        input_message_content = InputTextMessageContent("**need help 🤔**\nstart the bot in private") ,
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Join us🤗", url="https://t.me/mt_projectz")]])
		    ))])
 
    
async def checking(client, message):
	try:
		a = await app.get_chat_member("@mt_projectz", message.from_user.id)
		return True 
	except Exception as e:
		#await message.reply(e)
		return False

@app.on_message(filters.command("start"))
async def strf(client, message):
		chat_id = message.chat.id 
		user = collection.find_one({"user_id": chat_id})
		if user:
			await message.reply(f"👋Hello {message.from_user.mention} \n\nWelcome Restricted Messages Saver Bot🤖 This bot can help you to save restricted content from <b>public channels! Even upto 4GB file!</b>\n✨I can also work on inline mode✨\n<code>@RestrictedMessagesSaverBot your-link</code>\n🚀Just Send me the link of the message🕹", parse_mode = enums.ParseMode.HTML, reply_markup = key)
		else:
			collection.insert_one({"user_id": chat_id})
			await message.reply(f"👋Hello {message.from_user.mention} \n\nWelcome Restricted Messages Saver Bot🤖 This bot can help you to save restricted content from <b>public channels! Even upto 4GB file!</b>\n✨I can also work on inline mode✨\n<code>@RestrictedMessagesSaverBot your-link</code>\n🚀Just Send me the link of the message🕹", parse_mode = enums.ParseMode.HTML, reply_markup = key)

join = InlineKeyboardMarkup([
[InlineKeyboardButton(text ="🕹Join My Updates🕹", url="t.me/Mt_projectz")]
])

@app.on_message(filters.regex("http"))
async def send(client, message):
	check = await checking(client, message)
	if check == True:
		pass	 
	else:
		await message.reply("⚠️Dear in order to use this bot you must be a member of our channel!\nJoin and try again♻️", reply_markup = join)
		return
	try:
		s = str(message.text[13:])
		m = s.split("/")[0]
		s1 = f"@{m}"
		m1 = s.split("/")[1]
		a = await app.get_messages(s1, int(m1))	
		if a.photo:
			await app.send_photo(message.chat.id, a.photo.file_id, caption = message.caption)
			return 
		if a.document:				
			await app.send_document(message.chat.id, a.document.file_id, caption = a.caption)	
			return 
		if a.poll:
			await message.reply("🤨For Now I Don\'t Support Poll!")
			return 
		if a.video:						
			await app.send_video(message.chat.id, a.video.file_id, caption = message.caption)			
			return 
		if a.text:
			await message.reply(a.text)			
			return
		if a.audio:
			await app.send_audio(message.chat.id, a.audio.file_id, caption = message.caption)			
			return 
		if a.voice:
			await app.send_voice(message.chat.id, a.voice.file_id, caption = message.caption)			
			return 
		else:
			await message.reply("⚠️Either i don\'t know this type of content! or I couldn't save it.")
	except Exception as e:
		await message.reply("🔰Oppss! Make sure that the channel is public and the link is starts with <b>https://</b>", parse_mode = enums.ParseMode.HTML)	
	
def start_bot3():
  print("bot3 is ready!")
  app.run()