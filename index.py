from keys import API_ID,API_HASH
from pyrogram import Client
import os
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

os.chdir(application_path)

plugin = dict(root="plugins")

app = Client(name="test2",
             api_id=API_ID,
             api_hash=API_HASH,
             plugins=plugin)

app.run()

