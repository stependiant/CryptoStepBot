import logging
from telegram.ext import CallbackContext
from commands import binance_client
from db import get_all_subscriptions

logger = logging.getLogger(__name__)

async def subscription_job(context: CallbackContext):
    job = context.job
    user_id = job.context['user_id']
    coin = job.context['coin']
    try:
        symbol = coin if coin.endswith("USDT") else coin + "USDT"
        price_info = binance_client.get_symbol_ticker(symbol=symbol)
        await context.bot.send_message(
            chat_id=user_id,
            text=f"Обновление для {coin}: текущая цена {price_info['price']} USDT"
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"Ошибка обновления для {coin}: {str(e)}"
        )


async def news_job(context: CallbackContext):
    from db import get_news_subscriptions
    subscriptions = get_news_subscriptions()
    news_message = "Свежие новости крипторынка: [Здесь могла быть ваша новость]"
    for (user_id,) in subscriptions:
        try:
            await context.bot.send_message(chat_id=user_id, text=news_message)
        except Exception as e:
            logger.error(f"Ошибка отправки новости пользователю {user_id}: {e}")

async def schedule_subscriptions(job_queue):
    subs = get_all_subscriptions()
    for user_id, coin, interval in subs:
        job_queue.run_repeating(
            subscription_job,
            interval=interval,
            first=10,
            context={'user_id': user_id, 'coin': coin}
        )
