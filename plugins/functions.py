from plugins.functions import *
from .functions import *
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
import time
from pyrogram import enums
from pyrogram.types import ChatPrivileges 
from datetime import datetime
import asyncio
import sys
import os
import time
from datetime import datetime
import pytz
from keys import WATCH_LIST_PATH

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__)) + '\\..'

class LoopControl:
    def __init__(self):
        self.running = False

    async def start(self,c,m):
        if not self.running:
            self.running = True
            await m.reply_text('loop started')
            with open(f"{application_path}{WATCH_LIST_PATH}",'r') as file:
                channels = file.read()
            channels = channels.split('\n')
            print(channels)
            while self.running:
                await ABMmethod(c,channels)

    async def stop(self):
        if self.running:
            self.running = False

schedul = LoopControl()
status_message_id = -1

async def change_status_message_id(mid):
    global status_message_id
    status_message_id = mid

def starts_with(data):
    async def func(flt, c:Client, m:Message):
        try: return m.text.startswith(flt.data)
        except:return False
    return filters.create(func, data=data)


def get_time_in_iran(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    iran_tz = pytz.timezone('Asia/Tehran')
    iran_dt = dt.astimezone(iran_tz)
    formatted_time = iran_dt.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time

async def ABMmethod(c,channels):
    restricter = []
    banned = []

    for channel in channels:
        async for users in c.get_chat_members(chat_id=channel,filter=enums.ChatMembersFilter.BANNED):
            restricter.append(str(users.restricted_by.id))
            banned.append(str(users.user.id))

        if len(restricter) > 0:
            for admin in restricter:
                try:
                    await c.ban_chat_member(chat_id=channel, user_id=admin)
                    await c.unban_chat_member(chat_id=channel, user_id=admin)
                except Exception as e:
                    await c.send_message(text=str(e),chat_id='me')
                    continue
            for victim in banned:
                await c.unban_chat_member(chat_id=channel, user_id=victim)

            await c.send_message(text=f'you got attacked!\ncheck it out',chat_id='me')

        await asyncio.sleep(2)
    if status_message_id > 0:
        await c.edit_message_text(chat_id='me',message_id=status_message_id,text=f'last_check={get_time_in_iran(time.time())}\nchannels={channels}')

    

