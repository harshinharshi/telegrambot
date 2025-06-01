from telegram.ext import Application, MessageHandler, filters, CommandHandler
from dotenv import load_dotenv
import os

load_dotenv()

async def reply(update, context):
    await update.message.reply_text("Hello there!")

def main():
    """
    Handles the initial launch of the program (entry point).
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("No BOT_TOKEN found in environment variables")
    application = Application.builder().token(token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()
    application.add_handler(MessageHandler(filters.TEXT, reply))
    application.add_handler(CommandHandler("hello", reply))
    print("Telegram Bot started!", flush=True)
    application.run_polling()


if __name__ == '__main__':
    main()