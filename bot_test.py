import os
import logging
from telegram import Bot
from telegram.ext import Application, CallbackContext
import schedule
import time
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Token and proxy settings
TOKEN = '7023472542:AAG8pH1kznqySo77CPGJo-xg-K1LAGGhPMQ'

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

def send_morning_message(context: CallbackContext):
    today = datetime.now().day
    if today in dates_shift1:
        morning_workers = morning_shift1
    elif today in dates_shift2:
        morning_workers = morning_shift2
    else:
        return
    
    morning_message = "На смене (08:00-16:00):\n" + "\n".join(morning_workers)
    context.bot.send_message(chat_id=CHAT_ID, text=morning_message)

def send_evening_message(context: CallbackContext):
    today = datetime.now().day
    if today in dates_shift1:
        evening_workers = evening_shift1
    elif today in dates_shift2:
        evening_workers = evening_shift2
    else:
        return
    
    evening_message = "На смене (16:00-23:59):\n" + "\n".join(evening_workers)
    context.bot.send_message(chat_id=CHAT_ID, text=evening_message)

def check_likes(context: CallbackContext):
    # Логика для проверки лайков и отправки напоминаний
    pass

def main():
    application = Application.builder().token(TOKEN).build()

    # Планировщик для отправки сообщений в заданное время
    schedule.every().day.at("07:45").do(send_morning_message, CallbackContext(application))
    schedule.every().day.at("15:45").do(send_evening_message, CallbackContext(application))
    schedule.every().day.at("08:10").do(check_likes, CallbackContext(application))
    schedule.every().day.at("16:10").do(check_likes, CallbackContext(application))

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
