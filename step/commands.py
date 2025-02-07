import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from binance.client import Client
from binance.exceptions import BinanceAPIException
from config import BINANCE_API_KEY, BINANCE_API_SECRET
import db

logger = logging.getLogger(__name__)
# Инициализируем Binance в тестовом режиме
binance_client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)

# Пример единообразного стиля сообщений:
# Для успеха – "✅", для ошибок – "❌", для информации – "ℹ️", для команд – "🚀", для трендов – "📈/📉" и т.д.

async def start(update: Update, context: CallbackContext):
    """Команда /start – приветствие и краткая инструкция."""
    user = update.effective_user
    msg = (
        f"👋 Привет, {user.first_name}!\n\n"
        "🚀 Я крипто-бот для отслеживания рынка.\n"
        "ℹ️ Введи /help для списка команд."
    )
    await update.message.reply_text(msg)

async def help_command(update: Update, context: CallbackContext):
    msg = (
        "ℹ️ <b>Доступные команды:</b>\n\n"
        "👋 <code>/start</code> – Приветствие\n"
        "ℹ️ <code>/help</code> – Справка\n"
        "📜 <code>/all</code> – Список криптовалют\n"
        "💰 <code>/price &lt;монета&gt;</code> – Текущая цена\n"
        "📊 <code>/ticker &lt;монета&gt;</code> – 24-ч статистика\n"
        "📈 <code>/orderbook &lt;монета&gt;</code> – Стакан\n"
        "🕒 <code>/history &lt;монета&gt;</code> – История сделок\n"
        "🔄 <code>/converter &lt;сумма&gt; &lt;из_монеты&gt; &lt;в_монету&gt;</code> – Конвертация\n"
        "🔔 <code>/subscribe &lt;монета&gt; &lt;интервал&gt;</code> – Подписка\n"
        "❌ <code>/unsubscribe &lt;монета&gt;</code> – Отмена подписки\n"
        "📋 <code>/subscribe_list</code> – Список подписок\n"
        "🏆 <code>/top</code> – Лидеры рынка\n"
        "🤝 <code>/compare &lt;монета1&gt; &lt;монета2&gt;</code> – Сравнение\n"
        "📉 <code>/trends</code> – Рыночные тренды\n"
        "📰 <code>/news_on</code> – Вкл. новости\n"
        "🚫 <code>/news_off</code> – Выкл. новости\n"
    )
    await update.message.reply_text(msg, parse_mode='HTML')


async def get_all_coins():
    """Возвращает список монет, торгующихся к USDT."""
    info = binance_client.get_exchange_info()
    symbols = [s['symbol'] for s in info['symbols'] if s['symbol'].endswith('USDT')]
    return symbols

async def all_coins(update: Update, context: CallbackContext):
    """Команда /all – выводит список криптовалют."""
    try:
        symbols = await get_all_coins()
        symbols.sort()
        coins_text = "\n".join(symbols[:100])
        msg = f"📜 *Криптовалюты (100):*\n{coins_text}"
        await update.message.reply_text(msg, parse_mode='Markdown')
    except BinanceAPIException as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def price(update: Update, context: CallbackContext):
    """Команда /price <монета> – выводит текущую цену."""
    if len(context.args) != 1:
        await update.message.reply_text("❗ Использование: /price <монета>")
        return
    coin_input = context.args[0].upper()
    coin = coin_input if coin_input.endswith("USDT") else coin_input + "USDT"
    try:
        ticker_data = binance_client.get_symbol_ticker(symbol=coin)
        msg = f"💰 *{coin}* цена: *{ticker_data['price']} USDT*"
        await update.message.reply_text(msg, parse_mode='Markdown')
    except BinanceAPIException as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    except Exception:
        await update.message.reply_text(f"❌ Не удалось получить данные для {coin}")

async def ticker(update: Update, context: CallbackContext):
    """Команда /ticker <монета> – выводит 24-часовую статистику."""
    if len(context.args) != 1:
        await update.message.reply_text("❗ Использование: /ticker <монета>")
        return
    coin_input = context.args[0].upper()
    coin = coin_input if coin_input.endswith("USDT") else coin_input + "USDT"
    try:
        stats = binance_client.get_ticker(symbol=coin)
        msg = (
            f"📊 *{coin}* статистика за 24 часа:\n"
            f"💲 Цена: *{stats['lastPrice']} USDT*\n"
            f"🔄 Изм.: *{stats['priceChangePercent']}%*\n"
            f"📈 Макс.: *{stats['highPrice']} USDT*\n"
            f"📉 Мин.: *{stats['lowPrice']} USDT*\n"
            f"💹 Объем: *{stats['volume']}*\n"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')
    except BinanceAPIException as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    except Exception:
        await update.message.reply_text(f"❌ Не удалось получить данные для {coin}")

async def orderbook(update: Update, context: CallbackContext):
    """Команда /orderbook <монета> – выводит стакан."""
    if len(context.args) != 1:
        await update.message.reply_text("❗ Использование: /orderbook <монета>")
        return
    coin_input = context.args[0].upper()
    coin = coin_input if coin_input.endswith("USDT") else coin_input + "USDT"
    try:
        depth = binance_client.get_order_book(symbol=coin, limit=5)
        bids = "\n".join([f"💵 {bid[0]} (об: {bid[1]})" for bid in depth['bids']])
        asks = "\n".join([f"💶 {ask[0]} (об: {ask[1]})" for ask in depth['asks']])
        msg = f"📈 *{coin}* Order Book:\n\n*Покупки:*\n{bids}\n\n*Продажи:*\n{asks}"
        await update.message.reply_text(msg, parse_mode='Markdown')
    except BinanceAPIException as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    except Exception:
        await update.message.reply_text(f"❌ Не удалось получить данные для {coin}")

async def history(update: Update, context: CallbackContext):
    """Команда /history <монета> – выводит историю сделок."""
    if len(context.args) != 1:
        await update.message.reply_text("❗ Использование: /history <монета>")
        return
    coin_input = context.args[0].upper()
    coin = coin_input if coin_input.endswith("USDT") else coin_input + "USDT"
    try:
        trades = binance_client.get_recent_trades(symbol=coin, limit=5)
        msg = f"🕒 *{coin}* последние сделки:\n"
        for trade in trades:
            msg += f"⏰ {trade['time']} | 💲 {trade['price']} | 🔢 {trade['qty']}\n"
        await update.message.reply_text(msg, parse_mode='Markdown')
    except BinanceAPIException as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    except Exception:
        await update.message.reply_text(f"❌ Не удалось получить данные для {coin}")

async def converter(update: Update, context: CallbackContext):
    """Команда /converter <сумма> <из_монеты> <в_монету> – конвертирует валюты."""
    if len(context.args) != 3:
        await update.message.reply_text("❗ Использование: /converter <сумма> <из_монеты> <в_монету>")
        return
    try:
        amount = float(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Сумма должна быть числом")
        return
    from_coin = context.args[1].upper()
    to_coin = context.args[2].upper()
    from_symbol = from_coin if from_coin.endswith("USDT") else from_coin + "USDT"
    to_symbol = to_coin if to_coin.endswith("USDT") else to_coin + "USDT"
    try:
        from_price = float(binance_client.get_symbol_ticker(symbol=from_symbol)['price'])
        to_price = float(binance_client.get_symbol_ticker(symbol=to_symbol)['price'])
        result = amount * from_price / to_price
        msg = f"🔄 *{amount} {from_coin}* = *{result:.8f} {to_coin}*"
        await update.message.reply_text(msg, parse_mode='Markdown')
    except BinanceAPIException as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    except Exception:
        await update.message.reply_text("❌ Не удалось выполнить конвертацию")

async def subscribe(update: Update, context: CallbackContext):
    """
    Команда /subscribe <монета> <интервал> – подписка на обновления.
    Интервал указывается в секундах.
    """
    if len(context.args) != 2:
        await update.message.reply_text("❗ Использование: /subscribe <монета> <интервал_сек>")
        return
    coin = context.args[0].upper()
    try:
        interval = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Интервал должен быть числом")
        return
    user_id = update.effective_user.id
    db.add_subscription(user_id, coin, interval)
    await update.message.reply_text(f"✅ Подписка на *{coin}* установлена (интервал: {interval} сек)", parse_mode='Markdown')

async def unsubscribe(update: Update, context: CallbackContext):
    """Команда /unsubscribe <монета> – отмена подписки."""
    if len(context.args) != 1:
        await update.message.reply_text("❗ Использование: /unsubscribe <монета>")
        return
    coin = context.args[0].upper()
    user_id = update.effective_user.id
    db.remove_subscription(user_id, coin)
    await update.message.reply_text(f"✅ Подписка на *{coin}* отменена", parse_mode='Markdown')

async def subscribe_list(update: Update, context: CallbackContext):
    """Команда /subscribe_list – выводит список активных подписок."""
    user_id = update.effective_user.id
    subs = db.get_subscriptions(user_id)
    if not subs:
        await update.message.reply_text("ℹ️ У вас нет активных подписок")
    else:
        msg = "📋 *Ваши подписки:*\n"
        for coin, interval in subs:
            msg += f"• {coin} — {interval} сек\n"
        await update.message.reply_text(msg, parse_mode='Markdown')

async def top(update: Update, context: CallbackContext):
    """Команда /top – вывод рейтинга лидеров рынка по объёму торгов."""
    try:
        tickers = binance_client.get_ticker()
        sorted_tickers = sorted(tickers, key=lambda x: float(x['quoteVolume']), reverse=True)
        top_list = sorted_tickers[:5]
        msg = "🏆 *Топ по объёму торгов (24 ч):*\n"
        for t in top_list:
            msg += f"• {t['symbol']} — {t['quoteVolume']} | {t['priceChangePercent']}%\n"
        await update.message.reply_text(msg, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def compare(update: Update, context: CallbackContext):
    """Команда /compare <монета1> <монета2> – сравнение двух криптовалют."""
    if len(context.args) != 2:
        await update.message.reply_text("❗ Использование: /compare <монета1> <монета2>")
        return
    coin1 = context.args[0].upper()
    coin2 = context.args[1].upper()
    symbol1 = coin1 if coin1.endswith("USDT") else coin1 + "USDT"
    symbol2 = coin2 if coin2.endswith("USDT") else coin2 + "USDT"
    try:
        ticker1 = binance_client.get_ticker(symbol=symbol1)
        ticker2 = binance_client.get_ticker(symbol=symbol2)
        msg = (
            f"🤝 *Сравнение: {coin1} vs {coin2}*\n\n"
            f"• {coin1}: {ticker1['lastPrice']} USDT, {ticker1['priceChangePercent']}%\n"
            f"• {coin2}: {ticker2['lastPrice']} USDT, {ticker2['priceChangePercent']}%\n"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def trends(update: Update, context: CallbackContext):
    """Команда /trends – анализ рыночных трендов."""
    try:
        tickers = binance_client.get_ticker()
        sorted_by_change = sorted(tickers, key=lambda x: float(x['priceChangePercent']))
        losers = sorted_by_change[:3]
        gainers = sorted_by_change[-3:]
        msg = "📉 *Проигрывающие:*\n"
        for t in losers:
            msg += f"• {t['symbol']} — {t['priceChangePercent']}%\n"
        msg += "\n📈 *Набирающие:*\n"
        for t in reversed(gainers):
            msg += f"• {t['symbol']} — {t['priceChangePercent']}%\n"
        await update.message.reply_text(msg, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

async def news_on(update: Update, context: CallbackContext):
    """Команда /news_on – включает новостные оповещения."""
    user_id = update.effective_user.id
    db.add_news_subscription(user_id)
    await update.message.reply_text("📰 Новостные оповещения включены")

async def news_off(update: Update, context: CallbackContext):
    """Команда /news_off – отключает новостные оповещения."""
    user_id = update.effective_user.id
    db.remove_news_subscription(user_id)
    await update.message.reply_text("🚫 Новостные оповещения отключены")
