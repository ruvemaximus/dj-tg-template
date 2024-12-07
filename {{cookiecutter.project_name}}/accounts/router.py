import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

logger = logging.getLogger(__name__)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi!")


async def cmd_set_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = update.get_bot()
    await bot.delete_my_commands()
    await bot.set_my_commands([("start", "Начать диалог")])


HANDLERS = [
    CommandHandler("start", cmd_start),
    CommandHandler("set_commands", cmd_set_commands),
]
