import logging

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler
from tg.env import TOKEN


logger = logging.getLogger(__name__)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text & ~Filters.command, first_response)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(Filters.text & ~Filters.command, second_response)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop), CommandHandler("skip", skip)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?")

    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1
    # Оно указывает, что дальше на сообщения от этого пользователя
    # должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений
    # для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


# def skip(update, context):
#     update.message.reply_text("Перейдём к следующему вопросу")
#     return ConversationHandler.END


def first_response(update, context):
    # Это ответ на первый вопрос.
    # Мы можем использовать его во втором вопросе.
    locality = update.message.text
    if locality == '/skip':
        locality = 'у вас за окном'
        update.message.reply_text(
            "Какая погода у вас за окном")
    else:
        update.message.reply_text(
            "Какая погода в городе {locality}?".format(**locals()))
    # Следующее текстовое сообщение будет обработано
    # обработчиком states[2]
    return 2


def second_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    weather = update.message.text
    print(weather)
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными/


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()