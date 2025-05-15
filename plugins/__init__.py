from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
import time
from datetime import datetime
from plugins.functions import *
from keys import WATCH_LIST_PATH,LOG_PATH
from .safepost import check_post
import json

@Client.on_message(filters.command('start') & filters.me) 
async def slashstart(c:Client,m:Message):    
    await m.reply_text(text="""
                       type:
                       loop start , to start the anti ban member loop.
                       loop stop , to stop the loop
                       loop status , to constantly give you an update.
                       setch <channel username>, to add a chennel to watch list
                       clearch , removes all the channels""")

@Client.on_message(filters.regex('loop start') & filters.me) 
async def loopstart(c:Client,m:Message):
    await schedul.start(c,m)
    await m.reply_text(text="")

@Client.on_message(filters.regex('loop stop') & filters.me) 
async def loopstop(c:Client,m:Message):
    await schedul.stop()
    await m.reply_text(text="loop stopped")

@Client.on_message(filters.regex('loop status') & filters.me) 
async def loopstatus(c:Client,m:Message):
    message = await m.reply_text(text="ok!\nLet's check it out")
    await change_status_message_id(message.id)

@Client.on_message(starts_with('setch') & filters.me) 
async def setch(c:Client,m:Message):
    with open(f"{application_path}{WATCH_LIST_PATH}",'a') as file:
        file.write(m.text.split('\n')[1])
    await m.reply_text(text="ok!")

@Client.on_message(filters.regex('clearch') & filters.me) 
async def clearch(c:Client,m:Message):
    with open(f"{application_path}{WATCH_LIST_PATH}",'w') as file:
        file.write('')
    await m.reply_text(text="ok!")
    
@Client.on_message(filters.channel) 
async def clearch(c:Client,m:Message):
    with open(f"{application_path}{WATCH_LIST_PATH}",'r') as file:
        channels = file.read()
    channels = channels.split()
    print(m)
    print(channels)
    if f"@{m.sender_chat.username}" in channels:
        isok,data = await check_post(m)
        print(data,isok)
        with open(f"{application_path}{LOG_PATH}",'a',encoding="utf-8") as file:
            file.write(json.dumps(data,indent=4,ensure_ascii=False))
        if isok == 'False':
            await c.delete_messages(chat_id=m.sender_chat.id,message_ids=m.id)

