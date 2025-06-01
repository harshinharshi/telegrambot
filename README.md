# Telegram Finance Tracking Bot

A Telegram bot that helps users track their expenses and income through natural language processing. The bot uses OpenAI's GPT model to parse financial transactions and stores them in an Excel file.

## Features

- Natural language processing for expense/income tracking
- Automatic categorization of transactions
- Excel-based storage of financial data
- Easy-to-use Telegram interface

## Setup

1. Clone the repository:
```bash
git clone [<repository-url>](https://github.com/harshinharshi/telegrambot.git)
cd telegrambot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your credentials:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

5. Run the bot:
```bash
python bot.py
```
6. Telegram

1. Open Telegram and search for [@Test12091998Bot](https://t.me/Test12091998Bot)
2. Start a chat with the bot
3. Send your expense or income messages directly to the bot
eg: spent, 200, in Zudo clothing

## Usage

1. Start a chat with your bot on Telegram
2. Send messages describing your expenses or income, for example:
   - "Spent 500 on groceries at Walmart"
   - "Received 1000 from freelance work"
   - "250, KFC"

The bot will automatically:
- Parse the transaction details
- Categorize the expense/income
- Store the information in an Excel file
- Confirm the transaction

## Requirements

- Python 3.8+
- OpenAI API key
- Telegram Bot Token
- Required Python packages (see requirements.txt)

