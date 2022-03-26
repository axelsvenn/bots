from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from tg.env import TOKEN

start_keyboard = [['/dice', '/timer']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

dice_keyboard = [['hexagonal_cube', 'two_hexagonal_cubes'],
                 ['twenty-sided_cube', '/back']]
dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()

    updater.idle()


def start(update, context):
    update.message.reply_text(
        "Выберите что-то из двух.",
        reply_markup=start_markup
    )


def dice(update, context):
    update.message.reply_text(
        "Какой куб будем бросать?", reply_markup=dice_markup)


def timer(update, context):
    update.message.reply_text("Я готов работать все 24/7")


def back(update, context):
    return start(update, context)


if __name__ == '__main__':
    main()