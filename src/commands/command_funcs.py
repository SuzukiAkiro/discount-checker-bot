from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from src.commands import messages
from src.database.db_funcs import BotDB

db = BotDB("bot.sql")
ENTER_TEXT = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.add_user(update.effective_chat.id, update.effective_chat.username)
    db.init_watchlist(update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=messages.HELP)


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = db.parse_watchlist(user_id=update.effective_chat.id)
    answer = ""
    number = 1
    for tuples in result:
        url, price = tuples
        answer += f"{number}) Товар: {url}\n Цена: {price}\n\n"
        number += 1
    if answer:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=messages.LIST_EMPTY
        )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=messages.ADD)
    return ENTER_TEXT


async def save_text_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    user_items = db.parse_watchlist(user_id=update.effective_chat.id)
    for tuples in user_items:
        url, _ = tuples
        if msg == url:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=messages.ADD_ALREADY
            )
            return ConversationHandler.END
    if db.add_item(msg, update.effective_chat.id):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=messages.ADD_SUCCESS
        )
        return ConversationHandler.END
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=messages.ADD_FAILED
        )
        return ConversationHandler.END


async def remove_item(update: Update, context: ContextTypes):
    await list_command(update, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=messages.REMOVE
    )
    return ENTER_TEXT


async def save_text_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    user_items = db.parse_watchlist(user_id=update.effective_chat.id) 
    if not msg.startswith("https://"):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=messages.URL_ERROR 
        )
        return ConversationHandler.END
    for tuples in user_items:
        url, _ = tuples
        if msg == url:
            if db.remove_item(msg):
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=messages.REMOVE_SUCCESS
                )
                return ConversationHandler.END
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=messages.REMOVE_FAILED
                )
                return ConversationHandler.END
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=messages.REMOVE_ALREADY
    )
    return ConversationHandler.END
