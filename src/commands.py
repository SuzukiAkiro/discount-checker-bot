from src import messages, db_funcs
import aiosqlite
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await db_funcs.create_user(user_id=update.effective_user.id, user_name=str(update.effective_user.username))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=messages.HELP)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )
