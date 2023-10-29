import logging
from typing import NoReturn
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram import Update
import os
from exceptions import TokenInvalid

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
if not TELEGRAM_TOKEN:
    raise TokenInvalid()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.TEXT & ~(filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.run_polling()
