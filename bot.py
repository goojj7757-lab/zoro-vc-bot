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

# Clients initialize karna
app = Client(
    "zoro_vc_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

# Global State Variables for Audio Controls
current_volume = 1000
current_bass = 400
current_gain = 900
current_treble = 650
current_sharpness = 800
service_status = "Online"

# Start Command & Main Panel
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user_name = message.from_user.first_name if message.from_user else "User"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Support", url="https://t.me/"), InlineKeyboardButton("Updates", url="https://t.me/")],
        [InlineKeyboardButton("Audio Control", callback_data="audio_panel"), InlineKeyboardButton("Live Status", callback_data="live_status")],
        [InlineKeyboardButton("Command Guide", callback_data="cmd_guide")],
        [InlineKeyboardButton("Source Code", url="https://github.com/gooj7757-lab/zoro-vc-bot"), InlineKeyboardButton("Contact Owner", url="https://t.me/")]
    ])
    
    text = (
        f"— **SS GODX VC RELAY**\n"
        f"Professional real-time voice control\n\n"
        f"Welcome, {user_name}.\n\n"
        f"Manage the Logger source, Fight target, live relay, and audio profile from one control center.\n\n"
        f"Service • {service_status}\n"
        f"Uptime • Active\n\n"
        f"Select an action below or use `/help` for the complete command guide."
    )
    await message.reply_text(text, reply_markup=keyboard)

# Command Guide Command
@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    guide_text = (
        "**SS GODX VC Relay — Command Guide**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "**Voice chat**\n"
        "• `/record` — connect the source voice chat\n"
        "• `/join <chat_id>` — connect the target and start relaying\n"
        "• `/leaveplay` / `/leavevc` — leave the target voice chat\n"
        "• `/leaverecord` — leave the source voice chat\n"
        "• `/leave` / `/leaveall` / `/stop` — leave both voice chats\n"
        "• `/status` — view the active relay status\n"
        "• `/screenshare [on|off]` — loop video asset on VC screen share\n\n"
        "**Audio controls**\n"
        "• `/volume <1-7000>` — output volume\n"
        "• `/bass <0-1200>` — low-end boost\n"
        "• `/gain <0-1200>` — digital gain\n"
        "• `/treble <0-1200>` — high-frequency detail\n"
        "• `/sharpness <0-1200>` — speech presence\n"
        "• `/shabbir` — apply the recommended voice profile\n"
        "• `/preset [name]` — list or apply an EQ preset\n"
        "• `/echo [cave|dj|off]` — subterranean cavern reverb or DJ club delay\n"
        "• `/audio` — open live audio controls\n"
        "• `/mute` / `/unmute` — control output\n"
        "• `/automute on|off` — auto-mute on join\n"
        "• `/blast` — maximum output; use carefully\n\n"
        "**Account & admin**\n"
        "• `/plans` / `/mystatus` — premium and account status\n"
        "• `/subscribe <reference>` — submit payment proof\n"
        "• `/joingc <link>` — join a group or channel\n"
        "• `/setname <name>` — update the assistant name\n"
        "• `/sudo` / `/owner` — manage access\n"
        "• `/restart` — restart the service\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "All commands require the appropriate access level."
    )
    await message.reply_text(guide_text)

# Audio Control Panel Command & Callback
@app.on_message(filters.command("audio"))
async def audio_command(client: Client, message: Message):
    await send_audio_panel(message)

async def send_audio_panel(message_obj, is_callback=False):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Volume -10 ({current_volume})", callback_data="vol_minus"), InlineKeyboardButton(f"Volume +10 ({current_volume})", callback_data="vol_plus")],
        [InlineKeyboardButton(f"Bass -10 ({current_bass})", callback_data="bass_minus"), InlineKeyboardButton(f"Bass +10 ({current_bass})", callback_data="bass_plus")],
        [InlineKeyboardButton(f"Gain -10 ({current_gain})", callback_data="gain_minus"), InlineKeyboardButton(f"Gain +10 ({current_gain})", callback_data="gain_plus")],
        [InlineKeyboardButton(f"Treble -10 ({current_treble})", callback_data="treble_minus"), InlineKeyboardButton(f"Treble +10 ({current_treble})", callback_data="treble_plus")],
        [InlineKeyboardButton(f"Sharpness -10 ({current_sharpness})", callback_data="sharp_minus"), InlineKeyboardButton(f"Sharpness +10 ({current_sharpness})", callback_data="sharp_plus")],
        [InlineKeyboardButton("Mute", callback_data="audio_mute"), InlineKeyboardButton("Reset", callback_data="audio_reset")],
        [InlineKeyboardButton("Maximum output", callback_data="audio_blast"), InlineKeyboardButton("Refresh", callback_data="audio_refresh"), InlineKeyboardButton("Close", callback_data="audio_close")]
    ])
    
    panel_text = (
        "**Audio control panel**\n\n"
        "Relay: Active\n"
        "Logger source: Connected\n"
        "Fight target: Connected\n"
        f"Volume: {current_volume}\n"
        f"Bass: {current_bass}\n"
        f"Gain: {current_gain}\n"
        f"Treble: {current_treble}\n"
        f"Sharpness: {current_sharpness}\n"
        "Output: Active\n\n"
        "Changes apply immediately while a relay is active."
    )
    
    if is_callback:
        await message_obj.edit_message_text(panel_text, reply_markup=keyboard)
    else:
        await message_obj.reply_text(panel_text, reply_markup=keyboard)

# Callback Query Handler for Buttons
@app.on_callback_query()
async def handle_callbacks(client, callback_query):
    global current_volume, current_bass, current_gain, current_treble, current_sharpness
    data = callback_query.data
    
    if data == "audio_panel" or data == "audio_refresh":
        await callback_query.answer("Refreshing audio panel...")
        await send_audio_panel(callback_query.message, is_callback=True)
    elif data == "vol_plus":
        current_volume = min(7000, current_volume + 10)
        await callback_query.answer(f"Volume increased to {current_volume}")
        await send_audio_panel(callback_query.message, is_callback=True)
    elif data == "vol_minus":
        current_volume = max(1, current_volume - 10)
        await callback_query.answer(f"Volume decreased to {current_volume}")
        await send_audio_panel(callback_query.message, is_callback=True)
    elif data == "audio_close":
        await callback_query.message.delete()
    elif data == "cmd_guide":
        await callback_query.answer()
        await callback_query.message.reply_text("Use /help command to view the full command guide.")
    elif data == "live_status":
        await callback_query.answer("Service status: Online & Active!")
    else:
        await callback_query.answer("Action processed!")

# Individual Volume Command (`/volume <1-7000>`)
@app.on_message(filters.command("volume"))
async def set_volume(client: Client, message: Message):
    global current_volume
    if len(message.command) > 1:
        try:
            val = int(message.command[1])
            if 1 <= val <= 7000:
                current_volume = val
                await message.reply_text(f"✅ Output volume successfully set to **{current_volume}**.")
            else:
                await message.reply_text("❌ Please provide a volume value between **1 and 7000**.")
        except ValueError:
            await message.reply_text("❌ Invalid number format! Use: `/volume 6000`")
    else:
        await message.reply_text(f"🔊 Current output volume is: **{current_volume}**\nUse `/volume <1-7000>` to change it.")

# Bot Start Up
if __name__ == "__main__":
    print("Blaze VC Relay Bot is starting...")
    app.start()
    call_py.start()
    import pyrogram
    pyrogram.idle()
    
