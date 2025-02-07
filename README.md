# Crypto Telegram Bot 🚀

A Telegram bot that provides comprehensive cryptocurrency market data, deep analysis, and interactive features by integrating with the Binance API and using PostgreSQL for data storage. The bot offers a rich set of commands to retrieve real-time data, perform currency conversions, subscribe to periodic updates, and receive market news alerts.

## Features

### 1. General Menu and Help 🤖

- **/start**  
  **Function:** Initialization and Greeting 👋  
  **Description:** When this command is entered, the bot sends a welcome message, briefly explains its capabilities, and displays an interactive menu (e.g., using inline buttons) that allows quick access to desired functions.

- **/help**  
  **Function:** Command Help ℹ️  
  **Description:** This command displays a detailed list of all available commands along with their descriptions and usage examples, helping users quickly familiarize themselves with the bot's functionality.

---

### 2. Basic Cryptocurrency Information 💰

- **/all**  
  **Function:** Display a List of Cryptocurrencies 📜  
  **Description:** The command shows a list of all available cryptocurrencies (for example, those traded against USDT on Binance). The list may be sorted or paginated for ease of viewing.

- **/price `<coin>`**  
  **Function:** Get Current Price 💲  
  **Description:** When used with a cryptocurrency symbol (e.g., `/price BTC`), the bot fetches and displays the current price of the selected coin relative to USDT.

- **/ticker `<coin>`**  
  **Function:** 24-Hour Statistics 📊  
  **Description:** This command provides detailed information for the last 24 hours—including current price, percentage change, high, low, and trading volume—to help assess the coin's daily performance.

---

### 3. Deep Analysis and Market Data 📈

- **/orderbook `<coin>`**  
  **Function:** Display the Order Book 🗂  
  **Description:** The command requests and shows the current list of buy and sell orders for the selected cryptocurrency. The price and volume information allows users to evaluate market depth and liquidity.

- **/history `<coin>`**  
  **Function:** Trade History 🕒  
  **Description:** When executed, the bot displays the most recent trades for the specified cryptocurrency, including time, price, and trade volume, which helps in tracking market activity and trends.

---

### 4. Interactive and Auxiliary Functions 🔄

- **/converter `<amount>` `<from_coin>` `<to_coin>`**  
  **Function:** Currency Conversion 🔄  
  **Description:** This command converts a specified amount of one cryptocurrency into an equivalent amount of another at the current exchange rate (e.g., `/converter 0.5 BTC ETH`), providing a quick calculation of exchange values.

- **/subscribe `<coin>` `<interval>`**  
  **Function:** Subscribe to Regular Updates 🔔  
  **Description:** Allows users to subscribe to automatic updates for a selected cryptocurrency at a specified interval (e.g., every 15 minutes or 1 hour). The bot periodically sends updates on the current price and changes.

- **/unsubscribe `<coin>`**  
  **Function:** Unsubscribe ❌  
  **Description:** This command cancels a previously set subscription for the specified cryptocurrency, stopping the automatic updates.

- **/subscribe_list**  
  **Function:** View Active Subscriptions 📋  
  **Description:** The command displays a list of all active subscriptions for the user, showing details about the selected cryptocurrencies and update intervals, which helps manage current subscriptions.

---

### 5. Additional Commands and Market Analysis 🏆

- **/top**  
  **Function:** Market Leaders Ranking 🏆  
  **Description:** This command displays a list of top cryptocurrencies based on various criteria—such as the highest 24-hour gain, the highest trading volume, or the greatest liquidity—allowing users to quickly identify the most dynamic coins.

- **/compare `<coin1>` `<coin2>`**  
  **Function:** Compare Cryptocurrencies 🤝  
  **Description:** The command compares two cryptocurrencies by key parameters (current price, trading volume, percentage change, etc.) to help evaluate which coin might be more promising at the moment.

- **/trends**  
  **Function:** Market Trends Analysis 📉  
  **Description:** This command analyzes market data across the cryptocurrency market and highlights coins with the most significant changes (increases or decreases) over a chosen period, helping users grasp overall market dynamics and current trends.

---

### 6. News Notifications 📰

- **/news_on**  
  **Function:** Enable News Notifications 📰  
  **Description:** When invoked, the bot activates news notifications. Once enabled, the user will regularly receive important cryptocurrency market news (e.g., via push notifications or messages), keeping them informed of current events.

- **/news_off**  
  **Function:** Disable News Notifications 🚫  
  **Description:** This command disables news notifications, stopping the news feed so that users can customize their news update settings as desired.

---

## Technologies Used ⚙️

- **Python** – Programming language 🐍  
- **python-telegram-bot v20+** – Telegram Bot API framework 🤖  
- **python-binance** – Binance API client for Python 💹  
- **PostgreSQL** – Database for storing subscriptions and user data 🗄  
- **psycopg2** – PostgreSQL adapter for Python 🐘  
- **APScheduler** – Scheduling library for periodic tasks (integrated via the bot’s JobQueue) ⏰  
- **nest_asyncio** – Allows nested asyncio event loops (for compatibility in certain environments) 🔄  

---

## License

This project is licensed under the MIT License. 📄
