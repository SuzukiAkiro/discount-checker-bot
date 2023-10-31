from src import commands
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
import os
from exceptions import TokenInvalid

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
if not TELEGRAM_TOKEN:
    raise TokenInvalid()


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    list_handler = CommandHandler("tmp", commands.list)
    start_handler = CommandHandler("start", commands.start)
    help_handler = CommandHandler("help", commands.start)
    echo_handler = MessageHandler(filters.TEXT & ~(filters.COMMAND), commands.echo)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(list_handler)
    application.run_polling()
