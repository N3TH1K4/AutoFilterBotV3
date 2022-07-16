import re
import os
from os import environ

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = 'LuciferMoringstar_Robot'
API_ID = 18983092
API_HASH = "a6005a70e88369b4fb08b8350ebbdd35"
BOT_TOKEN = "1977805563:AAFgr7EsLJHqBTo8jOSxbU6bH8AMM8nTzTg"

# Bot settings
CACHE_TIME = 300
USE_CAPTION_FILTER = False

BROADCAST_CHANNEL = -1001558732171
ADMIN_ID = 1930645496
DB_URL = "mongodb+srv://TROJ3N:Nethika123@cluster0.uppg6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
BROADCAST_AS_COPY = True

# Admins, Channels & Users
ADMINS = 1930645496
CHANNELS = -1001553755993
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = ""
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]
TUTORIAL = "https://youtu.be/5hnYOKBzyi8"
# MongoDB information
DATABASE_URI = "mongodb+srv://TROJ3N:Nethika123@cluster0.uppg6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
DATABASE_NAME = "Tets"
COLLECTION_NAME = 'Telegram_files'

# Messages
default_start_msg = """
**Hi, I'm Auto Filter V3**

Here you can search files in Inline mode as well as PM, Use the below buttons to search files or send me the name of file to search.
"""
START_MSG = environ.get('START_MSG', default_start_msg)

FILE_CAPTION = ""
OMDB_API_KEY = ""
if FILE_CAPTION.strip() == "":
    CUSTOM_FILE_CAPTION=None
else:
    CUSTOM_FILE_CAPTION=FILE_CAPTION
if OMDB_API_KEY.strip() == "":
    API_KEY=None
else:
    API_KEY=OMDB_API_KEY
