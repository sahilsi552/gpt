usrs = ["me",491139,52670]
owner = 5935287
bot_token = "619148ePg71K4dTrTlUYfZ0sF4LYNpks_yc"
api_id = 7305
api_hash = "59c30695447f9016571ba9eb9d"
gpt_api = "sk-rgzTV2QOqpQy"

from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls.types import MediaStream


import websockets
from collections import Counter
from pyrogram import Client, filters 
from pyrogram.raw import functions, types
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import telethon
from telethon import TelegramClient, sync
from pyrogram.enums import ChatMemberStatus,ChatType
from async_eval import eval as async_eval
import datetime
import telegram
from telegram.ext import Application
from telegram.constants import ParseMode
import os
import io
import sys
import platform
import qrcode
import asyncio
import yt_dlp
from io import StringIO
import emoji
import math
import calendar
import socket
import requests
import random
import pickle
from SafoneAPI import SafoneAPI
import json
import gtts
import wget
import re
import PIL
from gtts import gTTS as tts
import speedtest
import pyrogram
from dotmap import DotMap
from tinydb import TinyDB, Query,where
from currency_converter import CurrencyConverter
import sqlite3
import pytz
from openai import AsyncOpenAI

sql = sqlite3.connect("sqlite.db")
fdb = TinyDB('filters.json')
db = TinyDB('db.json')
cc = CurrencyConverter()

sapi = SafoneAPI()

app = Client("spider",api_id,api_hash,workers=50) #pyrogram userbot client 
sapp = PyTgCalls(app)
sapp.start()
bot = Client("spider_bot",api_id,api_hash,bot_token=bot_token) # pyrogram bot client 
ptb = Application.builder().token(bot_token).concurrent_updates(8).connection_pool_size(16).build() #python-telegram-bot client 
tlbot = TelegramClient("telethon", api_id, api_hash)
tlbot.start(bot_token=bot_token)
client = AsyncOpenAI(api_key=gpt_api)
bot.start()
  

from urllib.request import urlopen,Request


async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")





@app.on_message(filters.text & filters.regex("^#gpt")) #& (filters.user(usrs) | filters.channel)
async def chatgpt(c,m):
 m.text = eval(f'f"""{m.text}"""')
 if m.text.split(" ")[1] == "img":
  if m.from_user.id == c.me.id:
   reply=await m.edit("ЁЯЦея╕П Generating...")
  else:
   reply=await m.reply("ЁЯЦея╕П Generating...")
  try:
    img = await client.images.generate(model="dall-e-3",prompt=" ".join(m.text.split(" ")[2:]),n=1,size="1024x1024")
  except Exception as e:
    return await reply.edit(e.message)
  await m.reply_photo(img.data[0].url,caption="**Result for** "+" ".join(m.text.split(" ")[2:]))
  await reply.delete()
 else:
   if m.from_user.id == c.me.id:
    reply=await m.edit("ЁЯЦея╕П Generating...")
   else:
    reply=await m.reply("ЁЯЦея╕П Generating...")
   response = await client.chat.completions.create(messages=[{"role": "user","content": " ".join(m.text.split(" ")[1:])}],model="gpt-4-turbo-preview")
   answer = "**Que. :** `" + " ".join(m.text.split(" ")[1:]) + "`\n\n**Result :** " + response.choices[0].message.content
   if len(answer) > 4090:
    return await reply.edit("тЭМ Result is exceed 4096 character limit..")
   await reply.edit(answer)

@app.on_edited_message(filters.text & filters.regex("^#ask") & (filters.user(usrs) | filters.channel))
async def edit(c,m):
  await chatgpt(c,m)

import time
@app.on_message(filters.command("dialog",prefixes=[".","!","/"]) & (filters.user(usrs) | filters.channel))
async def dialog(c,m):
 async for dialog in app.get_dialogs():
  if dialog.chat.type == pyrogram.enums.ChatType.PRIVATE and (await app.get_users(dialog.chat.id)).is_deleted == True:
   async for msg in app.get_chat_history(dialog.chat.id,limit=1):
    try:
     await app.invoke(pyrogram.raw.functions.messages.DeleteHistory(peer=(await app.resolve_peer(dialog.chat.id)),max_id=msg.id))
     print("Deleted")
     time.sleep(10)
    except Exception as a:
     print(a)
     time.sleep(10)
     continue



@app.on_message(filters.command("eval",prefixes=[".","!","/"]) & (filters.user(usrs) | filters.channel))
async def pm(client,message):
  global c,m
  c,m = client,message
  text = m.text[6:]
  try:
    vc = async_eval(text)
  except Exception as e:
    vc = str(e)
  try:
    await m.edit(f"Code : `{text}`\n\nResult : {str(vc)}",disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
  except Exception as e:
   try:
    await m.edit(f"Code : `{text}`\n\nResult : {str(e)}",disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
   except:
     pass
   with open("Result.txt" , "w") as g:
    g.writelines(str(vc))
    g.close()
   x = (await app.get_chat_member(m.chat.id,(await app.get_me()).id)).status if (m.chat.type == ChatType.SUPERGROUP) else None
   if (x == ChatMemberStatus.MEMBER) or (x == ChatMemberStatus.RESTRICTED):
     return
   try:
     await m.reply_document("Result.txt")
   except:
     return
@app.on_edited_message(filters.command("eval",prefixes=[".","!","/"]) & (filters.user(usrs) | filters.channel))
async def edit(c,m):
  await pm(c,m)

@app.on_message (filters.command("exec",prefixes=[".","!","/"]) & (filters.user(usrs) | filters.channel)) 
def compile_code(_,m): 
    output = StringIO() 
    sys.stdout= output
    code = m.text[6:]
    c = compile(code,"<string>","exec")
    try:
     exec(c)
    except:
     trace = traceback.format_exc()
     m.edit_text(f"Code:\n`{code}`\n\nTraceback: \n{trace}",disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)
    else:
        result = output.getvalue()
        m.edit_text(f"Code:\n`{code}`\n\nResult:\n{result if result else None}",disable_web_page_preview=True,parse_mode=pyrogram.enums.ParseMode.MARKDOWN)


@app.on_message(filters.command("addfilter",prefixes=[".","!","/"]) & (filters.user("me") | filters.channel))
async def addfilter(c,m):
  if len(m.text.split(" ")) > 1 and m.reply_to_message and m.reply_to_message.text:
    result = fdb.get(Query().cmd == m.text.split(" ")[1])
    if result:
      fdb.update({'cmd': m.text.split(" ")[1], "result" : m.reply_to_message.text.html}, Query().cmd == m.text.split(" ")[1])
      await m.edit("**Filter successfully updated!**")
      return
    fdb.insert({'cmd': m.text.split(" ")[1], "result" : m.reply_to_message.text.html})
    await m.edit("**Filter successfully added!**")
  else:
   await m.edit("**Invalid use of command!**")
   return
@app.on_message(filters.command("rmfilter",prefixes=[".","!","/"]) & (filters.user("me") | filters.channel))
async def rmfilter(c,m):
  if len(m.text.split(" ")) < 2:
   await m.edit("**Invalid use of command!**")
   return  
  try:
   result = fdb.remove(Query().cmd == m.text.split(" ")[1])
  except:
   result = None
  if result:
    await m.edit("**Filter removed successfully!**")
    return
  await m.edit("**No filter Found!**")
  
@app.on_message(filters.command("filters",prefixes=[".","!","/"]) & (filters.user("me") | filters.channel))
async def filter(c,m):
  try:
   result = ""
   i = 1
   for item in fdb:
    result = result + str(i) + ". " + item["cmd"]+"\n"
    i += 1
   result = "**ЁЯУЩ Available filters: **\n" + result
  except:
   result = None
  if result:
    await m.edit(result)
    return
  await m.edit("**No filters Found!**")
  
@app.on_message(filters.command("del",prefixes=[".","!","/"]) & (filters.user("me") | filters.channel))
async def delete(c,m):
  try:
   await m.delete()
   await m.reply_to_message.delete()
  except:
   return



@app.on_message(filters.user(usrs) | filters.channel)
async def rfilter(c,m):
  if not m.reply_to_message:
    return
  try:
   result = fdb.search(Query().cmd == m.text)[0]["result"]
  except:
   result = None
  if result:
     await m.reply_to_message.reply(result,quote=True, disable_web_page_preview=True)
     await m.delete()

idle()
