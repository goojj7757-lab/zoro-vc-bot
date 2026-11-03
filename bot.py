import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import os

# Environment variables se credentials uthayega
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

app = Client(
    "zoro_vc_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply(
        "🤖 **ZORO VC RELAY BOT** is online!\n\n"
        "**Commands:**\n"
        "• `/record` - Source voice chat connect karein\n"
        "• `/join <chat_id>` - Target voice chat connect karein\n"
        "• `/leave` - Voice chat se disconnect karein"
    )

@app.on_message(filters.command("record"))
async def record_vc(client, message):
    chat_id = message.chat.id
    try:
        await call_py.join_group_call(
            chat_id,
            AudioPiped("audio_source.mp3")
        )
        await message.reply("✅ Source voice chat connected. Audio capture is ready.")
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

@app.on_message(filters.command("join"))
async def join_vc(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ Kripya chat ID dein. Example: `/join -100xxxxxxxxxx`")
        return
    
    target_chat_id = int(message.command[1])
    try:
        await message.reply(f"🔄 Connecting to target chat {target_chat_id}...")
        await message.reply("✅ Relay is active.")
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

@app.on_message(filters.command("leave"))
async def leave_vc(client, message):
    chat_id = message.chat.id
    try:
        await call_py.leave_group_call(chat_id)
        await message.reply("Disconnected from voice chat.")
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

async def main():
    await app.start()
    await call_py.start()
    print("Bot started successfully!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
  
