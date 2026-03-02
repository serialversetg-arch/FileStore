import os

class Config(object):
    # --- API & Tokens ---
    API_ID = int(os.environ.get("API_ID", "12345"))
    API_HASH = os.environ.get("API_HASH", "your_api_hash")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
    
    # --- Database (MongoDB Atlas URL) ---
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://...") 
    OWNER_ID = int(os.environ.get("OWNER_ID", "12345678"))
    
    # --- Channels (Integers Only) ---
    FSUB_CHANNEL = int(os.environ.get("FSUB_CHANNEL", "-1002730333831")) 
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-100123456789")) 
    FSUB_ON = True 

    # --- Links ---
    CHNL_LNK = "https://t.me/Hindi_Tv_Verse"
    SUPP_LNK = "https://t.me/SerialVerse_support"

    # --- 🖼️ Premium Images ---
    START_IMAGES = [
        "https://i.ibb.co/S7609P4B/x.jpg",
        "https://i.ibb.co/G3Q974K3/x.jpg",
        "https://i.ibb.co/fzZTRQh8/x.jpg",
        "https://i.ibb.co/9Hnpgttg/x.jpg"
    ]
    FSUB_IMAGE = "https://i.ibb.co/S7609P4B/x.jpg"

    # --- 🎭 Stylish Texts ---
    START_MSG = "<b>✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ꜰɪʟᴇ sᴛᴏʀᴇ ✨\n\nʜᴇʟʟᴏ {user}, 👋</b>\n\n<i>ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ꜰɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ. sᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ, ᴀɴᴅ ɪ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ sʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ!</i>"
    
    FSUB_MSG = "<b>🛑 ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ 🛑\n\nʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜɴʟᴏᴄᴋ ᴛʜᴇ ꜰɪʟᴇs!</b>"
