from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from tg.env import TOKEN
import time


def echo(update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("time", time_bot))
    dp.add_handler(CommandHandler("data", data_bot))

    text_handler = MessageHandler(Filters.text, echo)

    dp.add_handler(text_handler)
    updater.start_polling()

    updater.idle()


def time_bot(update, context):
    update.message.reply_text(f"{time.strftime('%H:%M:%S')}")


def data_bot(update, context):
    update.message.reply_text(f"{time.strftime('%x')}")


if __name__ == '__main__':
    main()