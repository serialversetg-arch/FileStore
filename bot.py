import random, asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import UserNotParticipant, FloodWait, UserIsBlocked, InputUserDeactivated
from config import Config
from database import db

bot = Client("FileStoreBot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

user_data = {} # For Batch Mode

def main_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ᴜᴘᴅᴀᴛᴇs", url=Config.CHNL_LNK),
         InlineKeyboardButton("👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=Config.SUPP_LNK)],
        [InlineKeyboardButton("📜 ᴀʙᴏᴜᴛ ᴍᴇ", callback_data="about"),
         InlineKeyboardButton("🛡️ ʜᴇʟᴘ", callback_data="help")]
    ])

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await db.add_user(message.from_user.id) # Save User
    
    if Config.FSUB_ON:
        try:
            await client.get_chat_member(int(Config.FSUB_CHANNEL), message.from_user.id)
        except (UserNotParticipant, Exception):
            btn = [[InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=Config.CHNL_LNK)],
                   [InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ", url=f"https://t.me/{client.me.username}?start={message.command[1] if len(message.command) > 1 else ''}")]]
            return await message.reply_photo(photo=Config.FSUB_IMAGE, caption=Config.FSUB_MSG, reply_markup=InlineKeyboardMarkup(btn))

    await message.reply_photo(
        photo=random.choice(Config.START_IMAGES),
        caption=Config.START_MSG.format(user=message.from_user.mention),
        reply_markup=main_buttons()
    )

# --- 📢 BROADCAST ---
@bot.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def broadcast_handler(client, message):
    users = await db.get_all_users()
    msg = await message.reply_text("<code>Broadcasting...</code>")
    done, success, failed = 0, 0, 0
    async for user in users:
        try:
            await message.reply_to_message.copy(chat_id=int(user['id']))
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(chat_id=int(user['id']))
            success += 1
        except: failed += 1
        done += 1
    await msg.edit(f"<b>✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!</b>\n\nTotal: {done}\nSuccess: {success}\nFailed: {failed}")

# --- 📊 STATS ---
@bot.on_message(filters.command("stats") & filters.user(Config.OWNER_ID))
async def stats_handler(client, message):
    total = await db.total_users_count()
    await message.reply_text(f"<b>📊 Total Users:</b> <code>{total}</code>")

# --- 📁 BATCH & SINGLE FILE ---
@bot.on_message(filters.command("batch") & filters.user(Config.OWNER_ID))
async def batch_cmd(client, message):
    user_data[message.from_user.id] = []
    await message.reply_text("<b>✨ ʙᴀᴛᴄʜ ᴍᴏᴅᴇ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!</b>\nSend files now...", 
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏁 ꜰɪɴɪsʜ", callback_data="get_batch")]]))

@bot.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    if message.from_user.id in user_data:
        msg = await message.copy(Config.DB_CHANNEL)
        user_data[message.from_user.id].append(msg.id)
        await message.reply_text(f"✅ ᴀᴅᴅᴇᴅ: {len(user_data[message.from_user.id])}", quote=True)
    elif message.from_user.id == Config.OWNER_ID:
        msg = await message.copy(Config.DB_CHANNEL)
        link = f"https://t.me/{client.me.username}?start=file_{msg.id}"
        await message.reply_text(f"<b>✅ ʟɪɴᴋ:</b>\n<code>{link}</code>")

@bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    if query.data == "get_batch":
        ids = user_data.get(query.from_user.id)
        if not ids: return
        link = f"https://t.me/{client.me.username}?start=batch_{'-'.join(map(str, ids))}"
        await query.message.edit_text(f"<b>✅ ʙᴀᴛᴄʜ ʟɪɴᴋ:</b>\n<code>{link}</code>")
        del user_data[query.from_user.id]
    elif query.data == "back":
        await query.message.edit_caption(caption=Config.START_MSG.format(user=query.from_user.mention), reply_markup=main_buttons())
    # Add help/about callbacks here similarly

bot.run()
