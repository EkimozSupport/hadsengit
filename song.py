import os
import ffmpeg
import logging
import requests
import youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN

# logging
bot = Client(
   "Music-Bot",
   api_id=API_ID,
   api_hash=API_HASH,
   bot_token=BOT_TOKEN,
)
## Extra Fns -------
# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------
@bot.on_message(filters.command(['start']))
async def start(client, message):
       await message.reply("👋 Merhaba\n\nBen Hatıralara Müzik botu[🎶](https://telegra.ph/file/a0c4a5e178ac3bf74050e.jpg)\n\nKomutlarımı kanalımızda bulabilirsiniz... 😍🥰🤗\n\nJust 𝗧𝘆𝗽𝗲 a 𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲\n\n𝐄𝐠. `Believer`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('SAHİBİM', url='https://t.me/MangoSahip'),
                    InlineKeyboardButton('Kanal', url='https://t.me/kizilsancakbilgi')
                ]
            ]
        )
    )

@bot.on_message(filters.text)
def a(client, message):
    query=message.text
    print(query)
    m = message.reply('🔎 Şarkı Aranıyor...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. Aradığınız şarkıyı bulamadım 😐')
            return
    except Exception as e:
        m.edit(
            "❎ 𝐹𝑜𝑢𝑛𝑑 𝑁𝑜𝑡ℎ𝑖𝑛𝑔. 𝐒𝐨𝐫𝐫𝐲.\n\nAradıgınız Google de bulunmuyor.\n\nEg.`Believer`"
        )
        print(str(e))
        return
    m.edit("🔎 Şarkı Aranıyor ♫︎ 𝖯𝗅𝖾𝖺𝗌𝖾 𝖶𝖺𝗂𝗍 𝖿𝗈𝗋 𝖲𝗈𝗆𝖾 𝖲𝖾𝖼𝗈𝗇𝖽𝗌[🚀](https://telegra.ph/file/33e209cb838912e8714c9.mp4)")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep =  f'🎧 𝗧𝗶𝘁𝘁𝗹𝗲 : [{title[:35]}]({link})\n⏳ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 : `{duration}`\n👀 𝗩𝗶𝗲𝘄𝘀 : `{views}`\n\n📮 𝗕𝘆: {message.from_user.mention()}\n📤 𝗕𝘆 : @HatiralaraMusicbot'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('𝙁𝙖𝙞𝙡𝙚𝙙[❎](https://telegra.ph/file/98e2d7b14538a6308127f.mp4)\n\n Report This Erorr To Fix @Kizilsancakbilgi ❤️')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
