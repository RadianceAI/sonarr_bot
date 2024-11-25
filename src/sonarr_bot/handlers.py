import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

logger = logging.getLogger(__name__)

MAIN_MENU, NEW_DOWNLOAD, NEW_DOWNLOAD_INIT, NEW_DOWNLOAD_SEARCH, END = range(4)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Скачать сирик", "Загрузки"]]

    await update.message.reply_text(
        "Глааное меню",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return MAIN_MENU


async def new_download_init(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Введи сирик тогда")
    return NEW_DOWNLOAD_SEARCH


async def new_download_search(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    reply_keyboard = [[res] for res in ("a", "b", "c")]
    await update.message.reply_text(
        "Вот что удалось найти:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return MAIN_MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
