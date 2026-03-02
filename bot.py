import os
import random
import asyncio
import logging
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, FloodWait, UserIsBlocked, InputUserDeactivated
from config import Config
from database import db # Ensure database.py is in same folder

# Logging setup (Taaki error dikhe)
logging.basicConfig(level=logging.INFO)

# --- 🌐 Flask Web Server ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive! 🚀"

def run_web():
    try:
        app.run(host='0.0.0.0', port=8000)
    except Exception as e:
        logging.error(f"Flask Error: {e}")

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- 🤖 Telegram Bot ---
bot = Client(
    "FileStoreBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

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
    # User registration
    try:
        await db.add_user(message.from_user.id)
    except:
        pass
    
    # Check if link (e.g., /start file_123)
    if len(message.command) > 1:
        if Config.FSUB_ON:
            try:
                await client.get_chat_member(int(Config.FSUB_CHANNEL), message.from_user.id)
            except (UserNotParticipant, Exception):
                fsub_btn = [
                    [InlineKeyboardButton("📢 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ", url=Config.CHNL_LNK)],
                    [InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ", url=f"https://t.me/{client.me.username}?start={message.command[1]}")]
                ]
                return await message.reply_photo(
                    photo=Config.FSUB_IMAGE,
                    caption=Config.FSUB_MSG,
                    reply_markup=InlineKeyboardMarkup(fsub_btn)
                )
        
        # Link logic
        await message.reply_text("<b>⌛ ꜰᴇᴛᴄʜɪɴɢ ꜰɪʟᴇ...</b>")
        return

    # Normal Start
    await message.reply_photo(
        photo=random.choice(Config.START_IMAGES),
        caption=Config.START_MSG.format(user=message.from_user.mention),
        reply_markup=main_buttons()
    )

# --- 📢 Broadcast ---
@bot.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast_handler(client, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text("<code>Broadcasting...</code>")
    success, failed, done = 0, 0, 0
    async for user in users:
        try:
            await b_msg.copy(chat_id=int(user['id']))
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await b_msg.copy(chat_id=int(user['id']))
            success += 1
        except: failed += 1
        done += 1
    await sts.edit(f"<b>✅ Done!</b>\nSuccess: {success}\nFailed: {failed}")

# --- 📁 Batch Mode ---
@bot.on_message(filters.command("batch") & filters.user(Config.OWNER_ID))
async def batch_cmd(client, message):
    user_data[message.from_user.id] = []
    await message.reply_text("<b>Batch Mode ON!</b> Send files...", 
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏁 Finish", callback_data="get_batch")]]))

@bot.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    if message.from_user.id in user_data:
        msg = await message.copy(Config.DB_CHANNEL)
        user_data[message.from_user.id].append(msg.id)
        await message.reply_text(f"✅ Added: {len(user_data[message.from_user.id])}", quote=True)
    elif message.from_user.id == Config.OWNER_ID:
        msg = await message.copy(Config.DB_CHANNEL)
        link = f"https://t.me/{client.me.username}?start=file_{msg.id}"
        await message.reply_text(f"<b>✅ Link:</b>\n<code>{link}</code>")

@bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    if query.data == "about":
        await query.message.edit_caption(caption=Config.ABOUT_MSG, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]]))
    elif query.data == "help":
        await query.message.edit_caption(caption=Config.HELP_MSG, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]]))
    elif query.data == "back":
        await query.message.edit_caption(caption=Config.START_MSG.format(user=query.from_user.mention), reply_markup=main_buttons())
    elif query.data == "get_batch":
        ids = user_data.get(query.from_user.id)
        if not ids: return
        link = f"https://t.me/{client.me.username}?start=batch_{'-'.join(map(str, ids))}"
        await query.message.edit_text(f"<b>Batch Link:</b>\n<code>{link}</code>")
        del user_data[query.from_user.id]

# --- Start Sequence ---
if __name__ == "__main__":
    keep_alive()
    logging.info("Starting Bot...")
    bot.run()
