import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPulls, AudioQuality

# Environment Variables se credentials uthana
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")  # Assistant/Userbot ka session string

# 1. Bot Client (Commands aur Buttons ke liye)
app = Client(
    "zoro_vc_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# 2. Userbot Client (Voice Chat mein join karne ke liye assistant account)
userbot = Client(
    "zoro_assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# PyTgCalls Client initialize karna userbot ke sath
call_py = PyTgCalls(userbot)

current_volume = 1000

# Start Command & Main Menu
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Audio Control", callback_data="audio_panel"), InlineKeyboardButton("Live Status", callback_data="live_status")],
        [InlineKeyboardButton("Command Guide", callback_data="cmd_guide")],
        [InlineKeyboardButton("Source Code", url="https://github.com/gooj7757-lab/zoro-vc-bot")]
    ])
    
    text = (
        "🔥 **SS GODX VC RELAY PRO**\n"
        "Professional real-time voice control & streaming.\n\n"
        "Status: Online & Ready to Relay ⚡\n"
        "Use `/help` to see all available commands."
    )
    await message.reply_text(text, reply_markup=keyboard)

# Command Guide
@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    guide_text = (
        "**VC Relay — Command Guide**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "**Voice chat**\n"
        "• `/record` — connect the source voice chat\n"
        "• `/join <chat_id>` — connect the target and start relaying[span_1](start_span)[span_1](end_span)\n"
        "• `/leave` / `/stop` — leave voice chats[span_2](start_span)[span_2](end_span)\n"
        "• `/status` — view active relay status[span_3](start_span)[span_3](end_span)\n\n"
        "**Audio controls**\n"
        "• `/volume <1-7000>` — output volume[span_4](start_span)[span_4](end_span)\n"
        "• `/audio` — open live audio controls[span_5](start_span)[span_5](end_span)\n"
        "• `/mute` / `/unmute` — control output[span_6](start_span)[span_6](end_span)\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await message.reply_text(guide_text)

# Join Target Voice Chat (Relay Start)
@app.on_message(filters.command("join"))
async def join_voice_chat(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide the target chat ID!\nUsage: `/join <chat_id>`[span_7](start_span)[span_7](end_span)")
        return
    
    chat_id_input = message.command[1]
    try:
        chat_id = int(chat_id_input) if chat_id_input.startswith("-100") else chat_id_input
        
        # PyTgCalls ke zariye voice chat mein stream connect karna
        await call_py.join_group_call(
            chat_id,
            AudioPulls("https://icecast.liveatc.net/kjfk_twr"),  # Aap yahan apna audio source/stream URL de sakte hain
            quality=AudioQuality.STUDIO
        )
        await message.reply_text(f"✅ Successfully connected and started relaying to chat: `{chat_id}`")
    except Exception as e:
        await message.reply_text(f"❌ Failed to join voice chat!\nError: `{str(e)}`")

# Leave Voice Chat
@app.on_message(filters.command("leave") | filters.command("stop"))
async def leave_voice_chat(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        await call_py.leave_group_call(chat_id)
        await message.reply_text("🛑 Successfully left the voice chat and stopped relaying[span_8](start_span)[span_8](end_span).")
    except Exception as e:
        await message.reply_text(f"❌ Error: `{str(e)}`")

# Volume Control Command
@app.on_message(filters.command("volume"))
async def set_volume(client: Client, message: Message):
    global current_volume
    if len(message.command) > 1:
        try:
            val = int(message.command[1])
            if 1 <= val <= 7000:
                current_volume = val
                await message.reply_text(f"🔊 Output volume successfully set to **{current_volume}**.")
            else:
                await message.reply_text("❌ Please provide a volume value between **1 and 7000**[span_9](start_span)[span_9](end_span).")
        except ValueError:
            await message.reply_text("❌ Invalid format! Use: `/volume 6000`")
    else:
        await message.reply_text(f"🔊 Current output volume: **{current_volume}**\nUse `/volume <1-7000>` to change[span_10](start_span)[span_10](end_span).")

# Audio Panel Command
@app.on_message(filters.command("audio"))
async def audio_panel_cmd(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Volume ({current_volume})", callback_data="vol_info"), InlineKeyboardButton("Mute", callback_data="audio_mute")],
        [InlineKeyboardButton("Close", callback_data="audio_close")]
    ])
    await message.reply_text(
        "🎛️ **Audio Control Panel**\n\n"
        f"Volume: {current_volume}\n"
        "Output: Active",
        reply_markup=keyboard
    )

@app.on_callback_query()
async def callbacks(client, callback_query):
    if callback_query.data == "audio_close":
        await callback_query.message.delete()
    else:
        await callback_query.answer("Feature active!")

# Bot aur Userbot ko ek sath start karna
if __name__ == "__main__":
    print("Starting Zoro VC Relay Bot with Userbot & PyTgCalls...")
    userbot.start()
    call_py.start()
    app.start()
    import pyrogram
    pyrogram.idle()
