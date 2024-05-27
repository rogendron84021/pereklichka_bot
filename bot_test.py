import os
import logging
import httpx
from telegram import Bot
from telegram.ext import Application, CallbackContext
import schedule
import asyncio

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Token and proxy settings
TOKEN = os.getenv("TELEGRAM_TOKEN")
PROXY_URL = "http://64.23.150.202:8081"  # Example proxy

# Configure httpx client with proxy
client = httpx.AsyncClient(proxies=PROXY_URL)

# Initialize bot and application
bot = Bot(token=TOKEN)

async def send_message(context: CallbackContext, message: str):
    await context.bot.send_message(chat_id='YOUR_CHAT_ID', text=message)

async def send_morning_message(context: CallbackContext):
    morning_message = "Доброе утро! Начинаем смену."
    await send_message(context, morning_message)

async def send_evening_message(context: CallbackContext):
    evening_message = "Добрый вечер! Заканчиваем смену."
    await send_message(context, evening_message)

async def check_likes(context: CallbackContext):
    # Implement your logic to check likes
    pass

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    application = Application.builder().token(TOKEN).http_client(client).build()

    schedule.every().day.at("08:00").do(
        lambda: application.create_task(send_morning_message(CallbackContext(application))))
    schedule.every().day.at("20:00").do(
        lambda: application.create_task(send_evening_message(CallbackContext(application))))
    schedule.every().day.at("16:10").do(
        lambda: application.create_task(check_likes(CallbackContext(application))))

    # Start scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
