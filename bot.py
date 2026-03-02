import os
import random
import asyncio
import logging
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, FloodWait
from config import Config
from database import db

# --- 🌐 Flask Health Check ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive! 🚀"

def run_web(): app.run(host='0.0.0.0', port=8000)
def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- 🤖 Bot Client ---
bot = Client("FileStore", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

# --- ⌨️ Stylish Keyboards ---
def main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ᴜᴘᴅᴀᴛᴇs", url=Config.CHNL_LNK),
         InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=Config.SUPP_LNK)],
        [InlineKeyboardButton("📜 ᴀʙᴏᴜᴛ", callback_data="about"),
         InlineKeyboardButton("🛡️ ʜᴇʟᴘ", callback_data="help")]
    ])

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ", callback_data="back")]])

# --- 🏠 Start Handler ---
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await db.add_user(message.from_user.id)
    
    # Check if Link (Batch or Single)
    if len(message.command) > 1:
        data = message.command[1]
        
        # Smart FSub (Only for Links)
        if Config.FSUB_ON:
            try:
                await client.get_chat_member(int(Config.FSUB_CHANNEL), message.from_user.id)
            except (UserNotParticipant, Exception):
                btn = [[InlineKeyboardButton("📢 ᴊᴏɪɴ ɴᴏᴡ", url=Config.CHNL_LNK)],
                       [InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ", url=f"https://t.me/{client.me.username}?start={data}")]]
                return await message.reply_photo(photo=Config.FSUB_IMAGE, caption=Config.FSUB_MSG, reply_markup=InlineKeyboardMarkup(btn))

        # --- Link Logic (Batch or File) ---
        await message.reply_text("<b>⌛ ꜰᴇᴛᴄʜɪɴɢ ʏᴏᴜʀ ꜰɪʟᴇs...</b>")
        # Yahan forwarding logic (DB_CHANNEL se users tak)
        return

    # Normal Start
    await message.reply_photo(
        photo=random.choice(Config.START_IMAGES),
        caption=Config.START_MSG.format(user=message.from_user.mention),
        reply_markup=main_buttons()
    )

# --- 📂 Range Batch Feature ---
@bot.on_message(filters.command("batch") & filters.user(Config.OWNER_ID))
async def batch_range(client, message):
    # Instructions for Range Batch
    await message.reply_text(
        "<b>✨ ʀᴀɴɢᴇ ʙᴀᴛᴄʜ ᴍᴏᴅᴇ ✨</b>\n\n"
        "ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ <b>ꜰɪʀsᴛ ꜰɪʟᴇ ʟɪɴᴋ</b> ꜰʀᴏᴍ ʏᴏᴜʀ ᴅʙ ᴄʜᴀɴɴᴇʟ.\n\n"
        "<i>ɴᴏᴛᴇ: ᴍᴀᴋᴇ sᴜʀᴇ ᴛʜᴇ ʟɪɴᴋ ɪs ꜰʀᴏᴍ ᴛʜᴇ ᴅʙ ᴄʜᴀɴɴᴇʟ ʏᴏᴜ sᴇᴛ ɪɴ ᴄᴏɴꜰɪɢ.</i>"
    )
    # Temporary state for range batch
    client.set_state = "WAIT_FIRST_LINK"

@bot.on_message(filters.private & filters.text & filters.user(Config.OWNER_ID))
async def handle_links(client, message):
    if "t.me/" in message.text and "/start" not in message.text:
        try:
            # Extract Message ID from Telegram Link
            msg_id = int(message.text.split('/')[-1])
            
            if not hasattr(client, "first_id"):
                client.first_id = msg_id
                await message.reply_text("<b>✅ ꜰɪʀsᴛ ʟɪɴᴋ sᴀᴠᴇᴅ!</b>\n\nɴᴏᴡ sᴇɴᴅ ᴛʜᴇ <b>ʟᴀsᴛ ꜰɪʟᴇ ʟɪɴᴋ</b>.")
            else:
                last_id = msg_id
                first_id = client.first_id
                # Clear temp storage
                delattr(client, "first_id")
                
                batch_link = f"https://t.me/{client.me.username}?start=batch_{first_id}-{last_id}"
                await message.reply_text(
                    f"<b>✅ ʙᴀᴛᴄʜ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ!</b>\n\n"
                    f"<b>ꜰɪʀsᴛ ɪᴅ:</b> <code>{first_id}</code>\n"
                    f"<b>ʟᴀsᴛ ɪᴅ:</b> <code>{last_id}</code>\n\n"
                    f"🔗 <b>ʟɪɴᴋ:</b> <code>{batch_link}</code>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔗 sʜᴀʀᴇ ʟɪɴᴋ", url=f"https://t.me/share/url?url={batch_link}")]])
                )
        except Exception as e:
            await message.reply_text(f"❌ ᴇʀʀᴏʀ: `{e}`\nᴘʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴍᴇssᴀɢᴇ ʟɪɴᴋ.")

# --- 📢 Broadcast ---
@bot.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast_handler(client, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text("<code>🚀 ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...</code>")
    success, failed = 0, 0
    async for user in users:
        try:
            await b_msg.copy(chat_id=int(user['id']))
            success += 1
        except: failed += 1
    await sts.edit(f"<b>✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴅᴏɴᴇ!</b>\n\nsᴜᴄᴄᴇss: {success}\nꜰᴀɪʟᴇᴅ: {failed}")

# --- 🖱️ Callbacks (About, Help, Back) ---
@bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    if query.data == "about":
        await query.message.edit_caption(caption=Config.ABOUT_MSG, reply_markup=back_button())
    elif query.data == "help":
        await query.message.edit_caption(caption=Config.HELP_MSG, reply_markup=back_button())
    elif query.data == "back":
        await query.message.edit_caption(caption=Config.START_MSG.format(user=query.from_user.mention), reply_markup=main_buttons())
    await query.answer()

if __name__ == "__main__":
    keep_alive()
    bot.run()
