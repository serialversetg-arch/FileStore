import os

class Config(object):
    # --- API Details (Apni details bharein) ---
    API_ID = int(os.environ.get("API_ID", "12345"))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
    
    # --- Admin & Channels ---
    OWNER_ID = int(os.environ.get("OWNER_ID", "12345678"))
    FSUB_CHANNEL = int(os.environ.get("FSUB_CHANNEL", "-100...")) 
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-100..."))
    FSUB_ON = True 

    # --- Links ---
    CHNL_LNK = "https://t.me/Hindi_Tv_Verse"
    SUPP_LNK = "https://t.me/SerialVerse_support"

    # --- 🖼️ Images ---
    START_IMAGES = [
        "https://i.ibb.co/S7609P4B/x.jpg",
        "https://i.ibb.co/G3Q974K3/x.jpg",
        "https://i.ibb.co/fzZTRQh8/x.jpg",
        "https://i.ibb.co/9Hnpgttg/x.jpg"
    ]
    FSUB_IMAGE = "https://i.ibb.co/S7609P4B/x.jpg"

    # --- 🎭 1. Start Message ---
    START_MSG = """
<b>✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ꜰɪʟᴇ sᴛᴏʀᴇ ✨</b>

<b>ʜᴇʟʟᴏ {user}, 👋</b>

<i>ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ꜰɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ. sᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ, ᴀɴᴅ ɪ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ sʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ!</i>

<b>⚡ sᴛᴀᴛᴜs:</b> <code>ᴀᴄᴛɪᴠᴇ ✅</code>
<b>🛡️ sᴇᴄᴜʀɪᴛʏ:</b> <code>ʜɪɢʜ 🔒</code>
"""

    # --- 📢 2. Force Subscribe Message ---
    FSUB_MSG = """
<b>🛑 ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ 🛑</b>

<b>ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜɴʟᴏᴄᴋ ᴛʜᴇ ꜰɪʟᴇs!</b>

<i>ᴅᴜᴇ ᴛᴏ sᴇᴄᴜʀɪᴛʏ ʀᴇᴀsᴏɴs, ᴏɴʟʏ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ. ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴀɴᴅ ᴄʟɪᴄᴋ "ᴛʀʏ ᴀɢᴀɪɴ".</i>
"""

    # --- 📝 3. About Message ---
    ABOUT_MSG = """
<b>📝 ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ</b>

<b>● ɴᴀᴍᴇ:</b> <code>ꜰɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ</code>
<b>● ᴅᴇᴠᴇʟᴏᴘᴇʀ:</b> <a href='https://t.me/SerialVerse_support'>sᴇʀɪᴀʟ ᴠᴇʀsᴇ</a>
<b>● ᴄʜᴀɴɴᴇʟ:</b> <a href='https://t.me/Hindi_Tv_Verse'>ʜɪɴᴅɪ ᴛᴠ ᴠᴇʀsᴇ</a>

<b><i>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴅᴠᴀɴᴄᴇᴅ ᴄʟᴏᴜᴅ sᴇʀᴠᴇʀs ⚡</i></b>
"""

    # --- 🛠️ 4. Help Message ---
    HELP_MSG = """
<b>🛠️ ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs</b>

<b>• /start -</b> ᴛᴏ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ.
<b>• /batch -</b> ᴛᴏ ᴄʀᴇᴀᴛᴇ ʙᴀᴛᴄʜ ʟɪɴᴋ (ᴀᴅᴍɪɴ ᴏɴʟʏ).
<b>• ᴜᴘʟᴏᴀᴅ -</b> sᴇɴᴅ ᴀɴʏ ꜰɪʟᴇ ᴛᴏ ɢᴇᴛ ʟɪɴᴋ.

<b>⚠️ ɴᴏᴛᴇ:</b> ɪꜰ ʏᴏᴜ ꜰᴀᴄᴇ ᴀɴʏ ɪssᴜᴇ, ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ.
"""
