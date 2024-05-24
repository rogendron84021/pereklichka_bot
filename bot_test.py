from telegram import Bot, Update
from telegram.ext import Application, CallbackContext
import schedule
import time
import threading
import asyncio
from datetime import datetime
import os

# Токен вашего бота
TOKEN = os.getenv('TOKEN')

# Списки сотрудников
morning_shift1 = ['@vgxasc', '@unnamedT_T', '@IoannQuaker', '@neffertity81', '@galina_zh_86', '@Liubovalove', '@watashiwadare', '@NatalyaPark', '@Tanya_Y_2707', '@dzamila0505', '@SmirnIrina', '@angelina_elhova', '@EG06081986', '@ArishaV8', '@irinaa_0810', '@Zoyahka', '@IkyokoI']
evening_shift1 = ['@Lana_chance', '@KatiSmirnova', '@ylia_stanila', '@naxlex', '@Mother_of_tears', '@psilocibinum', '@natasha97s', '@lizezika', '@gulnaramagadeeva', '@kolibri89', '@Elizaveta_Shagina', '@viktoriavergi', '@ostrome', '@elgreat', '@vikt25', '@macaronischeese', '@teebdol']

morning_shift2 = ['@Vic_7toria', '@KatrinNex', '@Andrew_TM2', '@GrigoriuN', '@Evgenia_2608', '@Elina_1301', '@nadiy_asha', '@SyavkInn', '@Vitaminka005', '@Awster_gos', '@Sharshova', '@ralazar98', '@ansggar', '@EG06081986', '@galina_zh_86', '@dzamila0505', '@watashiwadare', '@IkyokoI']
evening_shift2 = ['@fogel0607', '@Gsjobss', '@Katrin_Uriev', '@shevtssovaa', '@NikolasVB', '@smp198', '@teebdol', '@entersoad', '@samoil84', '@DIVOLAN', '@Zoyahka', '@NatalieBallack', '@tewezaaaa', '@Evgenia_2608', '@Lana_chance']

# Даты смен
dates_shift1 = [2, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31]
dates_shift2 = [1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25, 28, 29]

# Идентификатор чата
CHAT_ID = -1001477285933  # Ваш chat_id

bot = Bot(token=TOKEN)

# Увеличение тайм-аута и размера пула соединений
request_kwargs = {
    "pool_timeout": 10.0,  # Увеличенный тайм-аут пула соединений
    "pool_size": 20,       # Увеличенный размер пула соединений
}

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
    elif сегодня в dates_shift2:
        evening_workers = evening_shift2
    else:
        return
    
    evening_message = "На смене (16:00-23:59):\n" + "\n".join(evening_workers)
    await context.bot.send_message(chat_id=CHAT_ID, text=evening_message)

async def check_likes(context: CallbackContext):
    today = datetime.now().day
    if today в dates_shift1:
        workers = morning_shift1 + evening_shift1
    elif сегодня в dates_shift2:
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
        # Предполагается, что у сообщения будут реакции (это может зависеть от используемой версии API Telegram)
        if hasattr(last_message, 'reactions'):
            for reaction в last_message.reactions:
                if reaction.emoji == '👍':
                    liked_users.update([user.username for user в reaction.users])

        # Проверка, кто не поставил лайк
        for worker in workers:
            if worker not in liked_users:
                await context.bot.send_message(chat_id=worker, text="Пожалуйста, отметься на перекличке!")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    application = Application.builder().token(TOKEN).request_kwargs(request_kwargs).build()

    # Планировщик для отправки сообщений в заданное время
    schedule.every().day.at("07:45").do(lambda: asyncio.run(send_morning_message(CallbackContext(application))))
    schedule.every().day.at("15:45").do(lambda: asyncio.run(send_evening_message(CallbackContext(application))))
    schedule.every().day.at("08:10").do(lambda: asyncio.run(check_likes(CallbackContext(application))))
    schedule.every().day.at("16:10").do(lambda: asyncio.run(check_likes(CallbackContext(application))))

    # Запуск планировщика в отдельном потоке
    threading.Thread(target=run_scheduler, daemon=True).start()

    application.run_polling()

if __name__ == '__main__':
    main()
