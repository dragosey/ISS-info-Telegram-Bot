from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from iss_requests import get_astronauts, get_nextISSpasses
from config import telegram_bots_key


def start(bot, update):
    update.message.reply_text(
        'Hello, {}!\nTo see all available commands use /help'.format(update.message.from_user.first_name))


def help(bot, update):
    update.message.reply_text(
        '/astronauts -> Return number of people currently in space along with their names and crafts.\n'
        '/issnextpass -> Shows next 5 passes of ISS above your current position. Location Access Permission required.\n'
        '/about -> Bot details and author credits.'
    )


def astronauts(bot, update):
    update.message.reply_text(get_astronauts())


def issnextpass(bot, update):
    keyboard = [[KeyboardButton("Send location", request_contact=False, request_location=True)]]
    update.message.reply_text('We need access to your current location!', reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True))


def about(bot, update):
    update.message.reply_text(
        'Created by: Dragos Sandu, github.com/dragosey\n'
        'Bot version: 1.0\n'
        'Developed as my first Telegram bot just to see how it works'
    )


def location(bot, update):
    if update.edited_message:
        location_details = update.edited_message.location
    else:
        location_details = update.message.location

    longitude = location_details.longitude
    latitude = location_details.latitude

    finalResponse = get_nextISSpasses(latitude, longitude)

    update.message.reply_text(finalResponse)


updater = Updater(telegram_bots_key)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('astronauts', astronauts))
updater.dispatcher.add_handler(CommandHandler('issnextpass', issnextpass))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(MessageHandler(Filters.location, location, edited_updates=True))

updater.start_polling()
updater.idle()
