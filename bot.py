import asyncio
from pymax import MaxClient, Message
from telegram import Bot

from config import (
    phone,
    TARGET_CHAT_ID,
    TARGET_USER_ID,
    TG_BOT_TOKEN,
    TG_CHAT_ID,
)

telegram_bot = Bot(token=TG_BOT_TOKEN)

# клиент PyMax
client = MaxClient(
    phone=phone,
    work_dir="cache",
    reconnect=False,
    logger=None
)

async def send_to_telegram(text: str):
    """Отправка текста в Telegram"""
    try:
        await telegram_bot.send_message(chat_id=TG_CHAT_ID, text=text)
    except Exception as e:
        print("Ошибка отправки в Telegram:", e)


@client.on_start
async def handle_start():
    print(f"Client started as: {client.me.names[0].first_name}")
    print(f"Listening only to chat_id = {TARGET_CHAT_ID} ...")


@client.on_message()
async def handle_message(message: Message) -> None:
    if message.chat_id != TARGET_CHAT_ID:
        return

    sender = getattr(message.sender, "names", None)
    if sender:
        sender_name = sender[0].first_name
    else:
        sender_name = str(message.sender)

    # только нужный пользователь(при необходимости)
    try:
        if int(sender_name) != TARGET_USER_ID:
            return
    except:
        return

    text = f"[БОСС В MAX] ЮЛЬКА ПИШЕТ: {message.text}"
    print(text)

    await send_to_telegram(text)


if __name__ == "__main__":
    try:
        asyncio.run(client.start())
    except KeyboardInterrupt:
        print("Client stopped by user")
