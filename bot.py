import os
import logging
import asyncio
import signal
import traceback
import platform
import ast
from typing import Optional
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from excel import append_to_excel
from datetime import datetime
from prompt import SYSTEM_PROMPT
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize OpenAI
llm = ChatOpenAI(
    temperature=0.1,
    model_name="gpt-3.5-turbo"
)

# Define the prompt template
template = """System: {system_prompt}

Question: {question}"""

prompt = ChatPromptTemplate.from_template(template)

# Create the chain
chain = (
    {
        "system_prompt": lambda _: SYSTEM_PROMPT,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_markdown_v2(
        f'Hi {user.mention_markdown_v2()}\! I\'m an AI\-powered assistant\. '
        f'Ask me anything and I\'ll do my best to help\!'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help information when the command /help is issued."""
    help_text = (
        "I'm here to help! Here's what you can do:\n\n"
        "• Just send me any question or message\n"
        "• I'll respond with helpful information\n"
        "• Use /start to get a welcome message\n"
        "• Use /help to see this message again"
    )
    await update.message.reply_text(help_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages and generate AI responses."""
    user_message = update.message.text
    
    try:
        # Show typing action
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )
        
        # Generate response
        response = chain.invoke(user_message)
        response_dict = ast.literal_eval(response)
        excel_entry = {'date': datetime.now().strftime('%Y-%m-%d'), **response_dict}
        append_to_excel(excel_entry)
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        await update.message.reply_text(
            "I apologize, but I encountered an error while processing your request. "
            "Please try again in a moment."
        )


async def error_handler(update: Optional[Update], context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "I apologize, but something went wrong. Please try again later."
        )


async def main() -> None:
    """Start the bot."""
    # Get bot token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
    
    # Create application
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.add_error_handler(error_handler)

    # Set up shutdown handling
    stop = asyncio.Event()
    
    def signal_handler():
        logger.info("Received shutdown signal")
        stop.set()
    
    # Platform-specific signal handling
    if platform.system() != 'Windows':
        for sig in (signal.SIGINT, signal.SIGTERM):
            asyncio.get_event_loop().add_signal_handler(sig, signal_handler)
    
    try:
        # Start the bot
        logger.info("Starting bot...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling(
            allowed_updates=Update.ALL_TYPES
        )
        logger.info("Bot is running!")
        
        # Wait for stop signal
        await stop.wait()
        logger.info("Shutdown signal received")
        
    except Exception as e:
        logger.error(f"Error during bot execution: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise
    finally:
        # Cleanup
        logger.info("Stopping bot...")
        await application.stop()
        await application.shutdown()
        logger.info("Bot stopped")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    finally:
        logger.info("Bot shutdown complete")                                                                      