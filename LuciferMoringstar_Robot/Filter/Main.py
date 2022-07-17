# (c) PR0FESS0R-99
from Config import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, TUTORIAL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from LuciferMoringstar_Robot import get_filter_results, get_file_details, is_subscribed, get_poster
from LuciferMoringstar_Robot import RATING, GENRES, HELP, ABOUT
import random
import requests
BUTTONS = {}
BOT = {}

anime_query = '''
   query ($id: Int,$page: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
            month
            day
          }
        endDate{
            year
            month
            day
            }
          episodes
          isLicensed
          recommendations(page:$page, perPage:10, sort:RATING_DESC,){
            pageInfo {
                lastPage
                total}
            edges{
                node{
                    mediaRecommendation{title{romaji}
                    coverImage{
              extraLarge}
              siteUrl
              averageScore
                    id}
                    rating
                }}
          }
          isAdult
          popularity
          source
          externalLinks{
              type
              url
              site
              language
              icon
              isDisabled
              }
          season
          type
          format
          status
          countryOfOrigin
          duration
          hashtag
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          nextAiringEpisode {
              timeUntilAiring
              episode
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          synonyms
          relations{
            edges{
                relationType
                node{
                    title{romaji}}
                    }
          }
          bannerImage
          coverImage{
              extraLarge}
          characters(page: $page, perPage: 25,sort:ROLE){
                pageInfo {
                    lastPage
                    total
              }
              edges{
                  node{
                    name{full}
                      }
                  role
                  }
                }
                  
      }
    }
'''
def shorten(description, info='anilist.co'):
    description = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        description += f'_{description}_[Read More]({info})'
    else:
        description += f"_{description}_"
    return description

def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]

url = 'https://graphql.anilist.co'
@Client.on_message(filters.command("anime") & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.command("anime") & filters.private & filters.incoming)
async def filter(client, message):
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sumanai, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Aaah Shit Happened!",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    #if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.command):
        #return
    if len(message.command) > 1:    
        btn = []
        search = message.text.split(None, 1)[1]
        files = await get_filter_results(query=search)
        variables = {'search': search}
        json = requests.post(url,json={
            'query': anime_query,
            'variables': variables}).json()
        if "errors" in json.keys():
            await client.send_message(user_id,"Anime not found")
            return
        search = search.replace('','_')
        json = json['data']['Media']
        titleen = json['title']['english']
        titleja = json['title']['romaji']
        score = json['averageScore']
        surl = json['siteUrl']
        tyype=json['format']
        idm = json.get("id")
        dura = json['duration']
        duration = f"{dura}  Minutes Per Ep."
        cover = json['coverImage']['extraLarge']
        syr = json['startDate']['year']
        smon = json['startDate']['month']
        sday = json['startDate']['day']
        airdate = f"{syr}.{smon}.{sday}"
        if smon and sday == None:
            airdate = f"not yet relesed Year That This Anime Gonna Relese is {syr}"
        elif syr == None:
            airdate ="Not Yet Announced"
        else:
            airdate = airdate
        endyr= json['endDate']['year']
        endmonth = json['endDate']['month']
        endday = json['endDate']['day']
        enddate = f"{endyr}.{endmonth}.{endday}"
        if endmonth and endday == None:
            enddate = f"The year This Anime finished was {endyr}"
        elif endyr == None:
            enddate = "Its Not Even Started"
        else:
            enddate =enddate
        country= json['countryOfOrigin']
        if country == "JP":
            country = "Japan 🇯🇵"
        elif country == "CN":
            country = "China 🇨🇳"
        else:
            country = country
        popp = json['popularity']
        popp = f"{popp} Anilist Users have This Anime In Their Lists"
        episodes= json.get('episodes', 'N/A')
        if json['nextAiringEpisode']:
              time = json['nextAiringEpisode']['timeUntilAiring'] * 1000
              time = t(time)
              newep = f"{json['nextAiringEpisode']['episode']} is Airing on {time}"
        else:
            newep = "Already Finished Or Not Relesed Yet"
        adult = json['isAdult']
        if adult == True:
            adult = " Yeah"
        else:
            adult = " Nope"
        genres = ""
        for x in json['genres']:
                genres += f"{x}, "
        genres = genres[:-2]
        genres = genres.replace("Action", "👊Action").replace("Adventure", "🏕Adventure").replace("Comedy", "😂Comedy").replace("Drama", "💃Drama").replace("Ecchi", "😘Ecchi").replace("Fantasy", "🧚🏻‍♂️Fantasy").replace("Hentai", "🔞Hentai").replace("Horror", "👻Horror").replace("Mahou Shoujo", "🧙Mahou Shoujo").replace("Mecha", "🚀Mecha").replace("Music", "🎸Music").replace("Mystery", "🔎Mystery").replace("Psychological", "😵‍💫Psychological").replace("Romance", "❤️Romance").replace("Sci-Fi", "🤖Sci-Fi").replace("Slice of Life", "🍃Slice of Life").replace("Sports", "⚽️Sports").replace("Supernatural", "⚡️Supernatural").replace("Thriller", "😳Thriller")                                                                       
        title_img = f"https://img.anili.st/media/{idm}"
        final_cap = f"""
`English Title:`  **{titleen}**
`Japanese Title:`  **{titleja}**
`Country:`  **{country}**
`Score:`  **{score}**
`Format:`  **{tyype}**
`Duration:`  **{duration}**
`Genres:`  **{genres}**
`Start Date:`  **{airdate}**
`End Date:`  **{enddate}**
`Episodes:`  **{episodes}**
`Popularity:`  **{popp}**
`Next Epi:`  **{newep}**
`Is Adult:`  **{adult}**
"""
        mo_tech_yt = f"{final_cap}\n\n"
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                filename=file.file_name.split(None, 0)[0]
                if "720p" in filename:
                    qua = "📌 720p"
                else:
                    qua = "📌 1080p"
                if "Sub" in filename:
                    du = "English Subbed"
                else:
                    du = "Dual Audio"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"pr0fess0r_99#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgUAAxkBAAIEv2LTgij7vceWNmOrs1oKJ4tWvjsOAAIsAgACFU2xVK6IRLzwatnPHgQ')
            await message.reply_text(f"I aint got  **{search}**  in my DBS")
            return
        mo_tech_yt = f"{final_cap}\n**{qua}** `{du}`"
        if not btn:
            await message.reply_text(f"I aint got  **{search}**  in my DBS")
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🖤 Pages 1/1",callback_data="pages")]
            )
            poster=cover
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⤐",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🖤 Pages 1/{data['total']}",callback_data="pages")]
        )
        poster=cover
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.command("sanime") & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.command("sanime") & filters.group & filters.incoming)
async def group(client, message):
    #if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        #return
    if len(message.command) > 2:    
        btn = []
        search = message.text.split(None, 1)[1]
        mo_tech_yt = f"Here's The Result For The Query **{search}**"
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=pr0fess0r_99_-_-_-_{file_id}")]
                )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgQAAxkBAAICeWK1MzZWqrA4kt0M2dB-FhPf7KRSAAJ-zQ8AAZXbYi-BuAYMW1yptR4E')
            await message.reply_text(f"I aint got  **{search}**  in my DBS")
            return
        
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📝 Pages 1/1",callback_data="pages")]
            )
            poster="https://static.zerochan.net/Archer.%28Ishtar%29.full.2803887.jpg"
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⤐",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📝 Pages 1/{data['total']}",callback_data="pages")]
        )
        poster="https://static.zerochan.net/Archer.%28Ishtar%29.full.2803887.jpg"
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("Kono Aho! You are using this for one of my old message, send the request again.. Aaah Mendokusei!",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⬷ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🖤 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⬷ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⤐", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🖤 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("Kono Aho! You are using this for one of my old message, send the request again.. Aaah Mendokusei!",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⤐", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🖤 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⬷ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⤐", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🖤 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("pr0fess0r_99"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption="Powered By: **@Otaku_Network**"
                    except Exception as e:
                        print(e)
                        f_caption="Powered By: **@Otaku_Network**"
                if f_caption is None: 
                    f_caption = "Powered By: **@Otaku_Network**"
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("Thanoshimiii!",show_alert=True)
