from src import messages 
from src.db_funcs import BotDB
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

db = BotDB("bot.sql")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.create_user(update.effective_chat.id, update.effective_chat.username)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=messages.HELP)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )
