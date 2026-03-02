import os
import random
import asyncio
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, FloodWait, UserIsBlocked, InputUserDeactivated
from config import Config
from database import db

# --- 🌐 Flask Web Server for Health Checks ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running! 🚀"

def run_web():
    # Koyeb/Heroku port 8000 use karte hain
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- 🤖 Telegram Bot Logic ---
bot = Client(
    "FileStoreBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

user_data = {} # For Batch Mode

# Common Buttons
def main_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚀 ᴜᴘᴅᴀᴛᴇs", url=Config.CHNL_LNK),
            InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=Config.SUPP_LNK)
        ],
        [
            InlineKeyboardButton("📜 ᴀʙᴏᴜᴛ ᴍᴇ", callback_data="about"),
            InlineKeyboardButton("🛡️ ʜᴇʟᴘ", callback_data="help")
        ]
    ])

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    # User ko DB mein add karna
    await db.add_user(message.from_user.id)
    
    # --- Force Subscribe Logic ---
    if Config.FSUB_ON:
        try:
            # ID ko integer mein convert karke check karna (Fixes Peer ID error)
            await client.get_chat_member(int(Config.FSUB_CHANNEL), message.from_user.id)
        except (UserNotParticipant, Exception):
            fsub_btn = [
                [InlineKeyboardButton("📢 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ", url=Config.CHNL_LNK)],
                [InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ", url=f"https://t.me/{client.me.username}?start={message.command[1] if len(message.command) > 1 else ''}")]
            ]
            return await message.reply_photo(
                photo=Config.FSUB_IMAGE,
                caption=Config.FSUB_MSG,
                reply_markup=InlineKeyboardMarkup(fsub_btn)
            )

    # Main Start Message
    await message.reply_photo(
        photo=random.choice(Config.START_IMAGES),
        caption=Config.START_MSG.format(user=message.from_user.mention),
        reply_markup=main_buttons()
    )

# --- 📢 BROADCAST FEATURE ---
@bot.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast_handler(client, message):
    all_users = await db.get_all_users()
    broadcast_msg = message.reply_to_message
    sts_msg = await message.reply_text("<code>🚀 Broadcast Started...</code>")
    
    success, failed, done = 0, 0, 0
    async for user in all_users:
        try:
            await broadcast_msg.copy(chat_id=int(user['id']))
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await broadcast_msg.copy(chat_id=int(user['id']))
            success += 1
        except (UserIsBlocked, InputUserDeactivated):
            failed += 1
        except Exception:
            failed += 1
        done += 1
        if done % 20 == 0:
            await sts_msg.edit(f"<b>ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ ᴘʀᴏɢʀᴇss...</b>\n\nTotal: {done}\nSuccess: {success}\nFailed: {failed}")

    await sts_msg.edit(f"<b>✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!</b>\n\nTotal: {done}\nSuccess: {success}\nFailed: {failed}")

# --- 📊 STATS COMMAND ---
@bot.on_message(filters.command("stats") & filters.user(Config.OWNER_ID))
async def stats_handler(client, message):
    total = await db.total_users_count()
    await message.reply_text(f"<b>📊 ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs:</b>\n\nTotal Users: <code>{total}</code>")

# --- 📁 BATCH MODE ---
@bot.on_message(filters.command("batch") & filters.user(Config.OWNER_ID))
async def batch_cmd(client, message):
    user_data[message.from_user.id] = []
    await message.reply_text(
        "<b>✨ ʙᴀᴛᴄʜ ᴍᴏᴅᴇ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!</b>\n\nsᴇɴᴅ ᴀʟʟ ꜰɪʟᴇs ᴏɴᴇ ʙʏ ᴏɴᴇ.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏁 ꜰɪɴɪsʜ ʙᴀᴛᴄʜ", callback_data="get_batch_link")]])
    )

# --- 📁 FILE HANDLING ---
@bot.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    if message.from_user.id in user_data:
        # Collecting for Batch
        msg = await message.copy(Config.DB_CHANNEL)
        user_data[message.from_user.id].append(msg.id)
        await message.reply_text(f"✅ ᴀᴅᴅᴇᴅ: <code>{len(user_data[message.from_user.id])}</code>", quote=True)
    elif message.from_user.id == Config.OWNER_ID:
        # Single File Upload
        msg = await message.copy(Config.DB_CHANNEL)
        link = f"https://t.me/{client.me.username}?start=file_{msg.id}"
        await message.reply_text(f"<b>✅ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ:</b>\n<code>{link}</code>")

# --- 🖱️ CALLBACK HANDLERS ---
@bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    if query.data == "about":
        await query.message.edit_caption(caption=Config.ABOUT_MSG, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back")]]))
    elif query.data == "help":
        await query.message.edit_caption(caption=Config.HELP_MSG, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="back")]]))
    elif query.data == "back":
        await query.message.edit_caption(caption=Config.START_MSG.format(user=query.from_user.mention), reply_markup=main_buttons())
    elif query.data == "get_batch_link":
        ids = user_data.get(query.from_user.id)
        if not ids:
            return await query.answer("Please send some files first!", show_alert=True)
        link = f"https://t.me/{client.me.username}?start=batch_{'-'.join(map(str, ids))}"
        await query.message.edit_text(f"<b>✅ ʙᴀᴛᴄʜ ʟɪɴᴋ:</b>\n<code>{link}</code>")
        del user_data[query.from_user.id]

# --- 🚀 RUN BOT ---
if __name__ == "__main__":
    keep_alive() # Starts Flask on Port 8000
    print("🚀 Bot and Web Server are Live!")
    bot.run()
