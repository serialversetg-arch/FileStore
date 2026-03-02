import os

class Config(object):
    # --- API & Tokens ---
    API_ID = int(os.environ.get("API_ID", "26910777"))
    API_HASH = os.environ.get("API_HASH", "8601f2f24993f6fdbcbac3bb27ceec38")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    
    # --- Database (MongoDB Atlas URL) ---
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://King:Cobra765592@cluster0.qy4m5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") 
    OWNER_ID = int(os.environ.get("OWNER_ID", "5232142502"))
    
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
