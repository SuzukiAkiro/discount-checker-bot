import logging
import os

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

from exceptions import TokenInvalid
from src.commands import command_funcs

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
if not TELEGRAM_TOKEN:
    raise TokenInvalid()

if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    list_handler = CommandHandler("list", command_funcs.list_command)
    start_handler = CommandHandler("start", command_funcs.start)
    help_handler = CommandHandler("help", command_funcs.start)
    add_handler = ConversationHandler(
        entry_points=[CommandHandler("add", command_funcs.add)],
        states={
            command_funcs.ENTER_TEXT: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND), command_funcs.save_text_add
                )
            ],
        },
        fallbacks=[list_handler, start_handler, help_handler],
    )
    remove_handler = ConversationHandler(
        entry_points=[CommandHandler("remove", command_funcs.remove_item)],
        states={
            command_funcs.ENTER_TEXT: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND), command_funcs.save_text_remove
                )
            ],
        },
        fallbacks=[list_handler, start_handler, help_handler],
    )

    application.add_handler(remove_handler)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(list_handler)
    application.add_handler(add_handler)
    application.run_polling()
