import logging
import asyncio
import nest_asyncio
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler
import config
import commands
import scheduler
import db

# Применяем nest_asyncio, чтобы разрешить повторный запуск цикла событий
nest_asyncio.apply()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    # Инициализируем базу данных (создаем таблицы, если их нет)
    db.init_db()

    # Создаем приложение через ApplicationBuilder
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    # Если JobQueue недоступна, значит extras не установлены
    if app.job_queue is None:
        raise RuntimeError("JobQueue не настроена. Установите python-telegram-bot с поддержкой job-queue, выполнив: pip install \"python-telegram-bot[job-queue]\"")

    # Задаем список команд бота
    command_list = [
        BotCommand("start", "Инициализация и приветствие"),
        BotCommand("help", "Справка по командам"),
        BotCommand("all", "Список криптовалют"),
        BotCommand("price", "Получение текущей цены монеты"),
        BotCommand("ticker", "24-часовая статистика"),
        BotCommand("orderbook", "Вывод стакана"),
        BotCommand("history", "Торговая история"),
        BotCommand("converter", "Конвертация валют"),
        BotCommand("subscribe", "Подписка на обновления"),
        BotCommand("unsubscribe", "Отмена подписки"),
        BotCommand("subscribe_list", "Список активных подписок"),
        BotCommand("top", "Рейтинг лидеров рынка"),
        BotCommand("compare", "Сравнение криптовалют"),
        BotCommand("trends", "Анализ рыночных трендов"),
        BotCommand("news_on", "Включить новостные оповещения"),
        BotCommand("news_off", "Отключить новостные оповещения")
    ]
    await app.bot.set_my_commands(command_list)

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", commands.start))
    app.add_handler(CommandHandler("help", commands.help_command))
    app.add_handler(CommandHandler("all", commands.all_coins))
    app.add_handler(CommandHandler("price", commands.price))
    app.add_handler(CommandHandler("ticker", commands.ticker))
    app.add_handler(CommandHandler("orderbook", commands.orderbook))
    app.add_handler(CommandHandler("history", commands.history))
    app.add_handler(CommandHandler("converter", commands.converter))
    app.add_handler(CommandHandler("subscribe", commands.subscribe))
    app.add_handler(CommandHandler("unsubscribe", commands.unsubscribe))
    app.add_handler(CommandHandler("subscribe_list", commands.subscribe_list))
    app.add_handler(CommandHandler("top", commands.top))
    app.add_handler(CommandHandler("compare", commands.compare))
    app.add_handler(CommandHandler("trends", commands.trends))
    app.add_handler(CommandHandler("news_on", commands.news_on))
    app.add_handler(CommandHandler("news_off", commands.news_off))

    # Планирование фоновых задач через job_queue, полученную из app.job_queue
    app.job_queue.run_repeating(scheduler.news_job, interval=5)
    scheduler.schedule_subscriptions(app.job_queue)

    # Запуск бота (polling)
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
