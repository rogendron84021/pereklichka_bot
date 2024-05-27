from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, CallbackContext
import schedule
import time
from datetime import datetime
import threading
import asyncio

# Токен вашего бота
TOKEN = '7023472542:AAG8pH1kznqySo77CPGJo-xg-K1LAGGhPMQ'

# Списки сотрудников
morning_shift1 = ['test']
evening_shift1 = ['test']

morning_shift2 = ['test']
evening_shift2 = ['test']

# Даты смен
dates_shift1 = [2, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31]
dates_shift2 = [1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25, 28, 29]

# Идентификатор чата
CHAT_ID = -1001477285933  # Ваш chat_id

async def send_morning_message(context: CallbackContext):
    today = datetime.now().day
    if today in dates_shift1:
        morning_workers = morning_shift1
    elif today in dates_shift2:
        morning_workers = morning_shift2
    else:
        return
    
    morning_message = "На смене (08:00-16:00):\n" + "\n".join(morning_workers)
    await context.bot.send_message(chat_id=CHAT_ID, text=morning_message)

async def send_evening_message(context: CallbackContext):
    today = datetime.now().day
    if today in dates_shift1:
        evening_workers = evening_shift1
    elif today in dates_shift2:
        evening_workers = evening_shift2
    else:
        return
    
    evening_message = "На смене (16:00-23:59):\n" + "\n".join(evening_workers)
    await context.bot.send_message(chat_id=CHAT_ID, text=evening_message)

async def check_likes(context: CallbackContext):
    today = datetime.now().day
    if today in dates_shift1:
        workers = morning_shift1 + evening_shift1
    elif today in dates_shift2:
        workers = morning_shift2 + evening_shift2
    else:
        return
    
    # Получение последних сообщений чата
    updates = await context.bot.get_updates()
    last_message = None
    for update in updates:
        if update.message and update.message.chat.id == CHAT_ID and "На смене" in update.message.text:
            last_message = update.message
            break

    if last_message:
        # Получение списка пользователей, которые поставили лайк
        liked_users = set()
        if last_message.reactions:
            for reaction in last_message.reactions:
                if reaction.emoji == '👍':
                    liked_users.update([user.username for user in reaction.users])

        # Проверка, кто не поставил лайк
        for worker in workers:
            if worker not in liked_users:
                await context.bot.send_message(chat_id=worker, text="Пожалуйста, отметься на перекличке!")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    application = Application.builder().token(TOKEN).build()

    # Планировщик для отправки сообщений в заданное время
    schedule.every().day.at("07:45").do(lambda: asyncio.run(send_morning_message(CallbackContext(application))))
    schedule.every().day.at("18:03").do(lambda: asyncio.run(send_evening_message(CallbackContext(application))))
    schedule.every().day.at("08:10").do(lambda: asyncio.run(check_likes(CallbackContext(application))))
    schedule.every().day.at("16:10").do(lambda: asyncio.run(check_likes(CallbackContext(application))))

    # Запуск планировщика в отдельном потоке
    threading.Thread(target=run_scheduler, daemon=True).start()

    application.run_polling()

if __name__ == '__main__':
    main()
