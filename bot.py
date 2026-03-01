import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant
from config import Config

bot = Client("FileStore", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

# Temporary batch storage
user_data = {}

def main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ᴜᴘᴅᴀᴛᴇs", url=Config.CHNL_LNK),
         InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=Config.SUPP_LNK)],
        [InlineKeyboardButton("📜 ᴀʙᴏᴜᴛ ᴍᴇ", callback_data="about"),
         InlineKeyboardButton("🛡️ ʜᴇʟᴘ", callback_data="help")]
    ])

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    if Config.FSUB_ON:
        try:
            await client.get_chat_member(Config.FSUB_CHANNEL, message.from_user.id)
        except UserNotParticipant:
            btn = [[InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=Config.CHNL_LNK)],
                   [InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ", url=f"https://t.me/{client.me.username}?start={message.command[1] if len(message.command) > 1 else ''}")]]
            return await message.reply_photo(photo=Config.FSUB_IMAGE, caption=Config.FSUB_MSG, reply_markup=InlineKeyboardMarkup(btn))

    await message.reply_photo(
        photo=random.choice(Config.START_IMAGES),
        caption=Config.START_MSG.format(user=message.from_user.mention),
        reply_markup=main_buttons()
    )

@bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    if query.data == "about":
        await query.message.edit_caption(caption=Config.ABOUT_MSG, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back")]]))
    elif query.data == "help":
        await query.message.edit_caption(caption=Config.HELP_MSG, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back")]]))
    elif query.data == "back":
        await query.message.edit_caption(caption=Config.START_MSG.format(user=query.from_user.mention), reply_markup=main_buttons())

bot.run()
