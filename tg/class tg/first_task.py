from telegram.ext import Updater, MessageHandler, Filters
from tg.env import TOKEN


def echo(update, context):
    update.message.reply_text(f"Я получил сообщение {update.message.text}")


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)

    dp.add_handler(text_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()