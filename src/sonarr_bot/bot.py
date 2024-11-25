from os import environ as env
from dotenv import load_dotenv

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from . import handlers

load_dotenv()


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(env["TOKEN"]).build()

    new_download_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.ALL, handlers.new_download_init)],
        states={
            handlers.NEW_DOWNLOAD_SEARCH: [
                MessageHandler(filters.TEXT, handlers.new_download_search)
            ]
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
        map_to_parent={
            handlers.NEW_DOWNLOAD: handlers.NEW_DOWNLOAD,
            handlers.MAIN_MENU: handlers.MAIN_MENU,
        },
    )

    main_menu_handlers = [
        new_download_handler,
    ]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("main_menu", handlers.main_menu)],
        states={
            handlers.MAIN_MENU: main_menu_handlers,
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
