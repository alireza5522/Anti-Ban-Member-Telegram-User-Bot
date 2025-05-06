from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
import time
from datetime import datetime
from plugins.functions import *
from keys import WATCH_LIST_PATH

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
    