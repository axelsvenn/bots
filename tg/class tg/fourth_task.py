from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from tg.env import TOKEN
from random import randint

start_keyboard = [['/dice', '/timer']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)

dice_keyboard = [['/hexagonal_cube', '/two_hexagonal_cubes'],
                 ['/twenty_sided_cube', '/start']]
dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)

timer_keyboard = [['/timer_30', '/timer_60'],
                 ['/timer_300', '/start']]
timer_markup = ReplyKeyboardMarkup(timer_keyboard, one_time_keyboard=False)

close_markup = ReplyKeyboardMarkup([["/close"]], one_time_keyboard=False)
current_time = 30


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("hexagonal_cube", hexagonal_cube))
    dp.add_handler(CommandHandler("two_hexagonal_cubes", two_hexagonal_cubes))
    dp.add_handler(CommandHandler("twenty_sided_cube", twenty_sided_cube))
    dp.add_handler(CommandHandler("timer", timer))
    dp.add_handler(CommandHandler("close", close))
    dp.add_handler(CommandHandler("timer_30", timer_30))
    dp.add_handler(CommandHandler("timer_60", timer_60))
    dp.add_handler(CommandHandler("timer_300", timer_300))

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


def hexagonal_cube(update, context):
    update.message.reply_text(randint(1, 6))


def two_hexagonal_cubes(update, context):
    update.message.reply_text(f"{randint(1, 6)} {randint(1, 6)}")


def twenty_sided_cube(update, context):
    update.message.reply_text(randint(1, 20))


def timer(update, context):
    update.message.reply_text(
        "На сколько секунд будем ставить таймер?", reply_markup=timer_markup)


def timer_30(update, context):
    set_timer(update, context, 30)


def timer_60(update, context):
    set_timer(update, context, 60)


def timer_300(update, context):
    set_timer(update, context, 300)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update, context, due):
    """Добавляем задачу в очередь"""
    global current_time
    current_time = due
    chat_id = update.message.chat_id
    context.job_queue.run_once(
        task,
        due,
        context=chat_id,
        name=str(chat_id)
    )
    text = f'засек {current_time} секунд!'
    update.message.reply_text(text, reply_markup=close_markup)


def task(context):
    job = context.job
    context.bot.send_message(job.context, text=f'{current_time} секунд истекло', reply_markup=timer_markup)


def close(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Хорошо, вернулся сейчас!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text, reply_markup=timer_markup)


if __name__ == '__main__':
    main()