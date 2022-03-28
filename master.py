import random
import os
import logging
import sys

from telegram.ext import Updater, CommandHandler
import telegram

from dotenv import load_dotenv


load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Добавляем файловый лог
fileHandler = logging.FileHandler('homework.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
# Добавляем вывод лога в консоль
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


def ret_int_num_step_10(initial, final, step_num):
    return random.randrange(initial, final, step_num).__str__()


def ret_int_num(initial, final):
    return random.randint(initial, final).__str__()


def send_message(update, context, initial, final, step_num=0):
    chat = update.effective_chat

    if step_num == 0:
        answer = ret_int_num(initial, final)
    else:
        answer = ret_int_num_step_10(initial, final, step_num)

    try:
        context.bot.send_message(chat_id=chat.id, text=answer)
        logger.info(f'Бот отправил сообщение {answer}')
    except telegram.error.TelegramError as error:
        logger.error(f'Не удалось отправить сообщение в телеграмм: {error}')


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = telegram.ReplyKeyboardMarkup([
        [
            '/D100_st10',
            '/D20',
            '/D10',
            '/D8',
            '/D6',
            '/D4',
            '/D3'
        ],
        [
            '/start',
            '/help'
        ]
    ], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Я помогу тебе!'.format(name),
        reply_markup=button
    )


def D_100_st_10(update, context):
    send_message(update, context, 10, 110, 10)


def D_20(update, context):
    send_message(update, context, 1, 20)


def D_10(update, context):
    send_message(update, context, 0, 9)


def D_8(update, context):
    send_message(update, context, 1, 8)


def D_6(update, context):
    send_message(update, context, 1, 6)


def D_4(update, context):
    send_message(update, context, 1, 4)


def D_3(update, context):
    send_message(update, context, 1, 3)


def send_help(update, context):
    chat = update.effective_chat
    answer = ('# D100_st10 - от 10 до 100 с шагом 10\n'
              '# D20 - от 1 до 20\n'
              '# D10 - от 0 до 9\n'
              '# D8 - от 1 до 8\n'
              '# D6 - от 1 до 6\n'
              '# D4 - от 1 до 4\n'
              '# D3 - от 1 до 3\n')
    context.bot.send_message(chat_id=chat.id, text=answer)


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('D100_st10', D_100_st_10))
    updater.dispatcher.add_handler(CommandHandler('D20', D_20))
    updater.dispatcher.add_handler(CommandHandler('D10', D_10))
    updater.dispatcher.add_handler(CommandHandler('D8', D_8))
    updater.dispatcher.add_handler(CommandHandler('D6', D_6))
    updater.dispatcher.add_handler(CommandHandler('D4', D_4))
    updater.dispatcher.add_handler(CommandHandler('D3', D_3))
    updater.dispatcher.add_handler(CommandHandler('help', send_help))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
