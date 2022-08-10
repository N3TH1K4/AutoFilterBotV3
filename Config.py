import re
import os
from os import environ

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = 'Nobara_Kugisakii'
API_ID = 18983092
API_HASH = "a6005a70e88369b4fb08b8350ebbdd35"
BOT_TOKEN = "5346281142:AAGyQRPmb-teZrkI8AaJnSRDWxVdfJbrvuc"

# Bot settings
CACHE_TIME = 300
USE_CAPTION_FILTER = False

BROADCAST_CHANNEL = -1001558732171
ADMIN_ID = 5592337870
DB_URL = "mongodb+srv://TROJ3N:Nethika123@cluster0.uppg6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
BROADCAST_AS_COPY = True

# Admins, Channels & Users
ADMINS = 5592337870
CHANNELS = -1001740801934
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = ""
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]
TUTORIAL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# MongoDB information
DATABASE_URI = "mongodb+srv://TROJ3N:Nethika123@cluster0.uppg6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
DATABASE_NAME = "nobara_kugisakii"
COLLECTION_NAME = 'ongoing_animee'

# Messages

START_MSG = """
**Hello** I'm Nobara Kugisaki
You can get anime using me! Use `/search anime_name` to search an anime
Inline Mode Is also Working

**NOTE:** I can Only give animes in @Airing_Anime_ON  

"""

FILE_CAPTION = "**Powered By: **@Otaku_network**"
OMDB_API_KEY = ""
if FILE_CAPTION.strip() == "":
    CUSTOM_FILE_CAPTION=None
else:
    CUSTOM_FILE_CAPTION=FILE_CAPTION
if OMDB_API_KEY.strip() == "":
    API_KEY=None
else:
    API_KEY=OMDB_API_KEY
