from telethon import TelegramClient, events
import sqlite3
import asyncio

# تنظیمات تلگرام
api_id = 29646851
api_hash = '70a40f9db30071a7be02eb35fef561b6'
phone_number = '+989155841124'

# ایجاد کلاینت تلگرام
client = TelegramClient('session_name', api_id, api_hash)

# لیست block_reply
block_reply = [
    101512739, 1622957174, 133450983, 1499394623,
    736768510, 93983470, 725484841, 58107887, 349942915
]

# تنظیم پایگاه داده SQLite
conn = sqlite3.connect("inputs.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS inputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        total_flow TEXT,
        duration TEXT
    )
""")
conn.commit()

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # شرایط مورد نظر: پیام باید خصوصی باشد، فرستنده نباید در block_reply باشد و ربات نباشد.
    if not event.is_private or event.sender_id in block_reply:
        return
    sender = await event.get_sender()
    if sender and sender.bot:
        return

    try:
        text = event.raw_text.strip()
        parts = text.split(',')
        if len(parts) == 3:
            client_name_input = parts[0].strip()
            total_flow_input = parts[1].strip()
            duration_input = parts[2].strip()
            cursor.execute("INSERT INTO inputs (client_name, total_flow, duration) VALUES (?, ?, ?)",
                           (client_name_input, total_flow_input, duration_input))
            conn.commit()
            await event.reply("اطلاعات دریافت و ذخیره شد.")
            await client.disconnect()
        else:
            await event.reply("فرمت پیام نادرست است. لطفاً به صورت: client_name, total_flow, duration ارسال کنید.")
    except Exception as e:
        await event.reply("خطا در پردازش پیام: " + str(e))

client.start(phone=phone_number)
client.run_until_disconnected()
conn.close()
