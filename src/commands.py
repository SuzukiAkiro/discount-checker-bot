from telegram import Update
from telegram.ext import ContextTypes

from src import messages
from src.db_funcs import BotDB

db = BotDB("bot.sql")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.add_user(update.effective_chat.id, update.effective_chat.username)
    db.init_watchlist(update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=messages.HELP)


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = db.parse_watchlist(update.effective_chat.id)
    answer = ""
    for tuples in result:
        url, price = tuples
        answer += f"Товар: {url}\n Цена: {price}\n\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )
