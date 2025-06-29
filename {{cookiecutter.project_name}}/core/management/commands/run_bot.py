import logging
from importlib import import_module
from os import environ

from django.conf import settings
from django.core.management import BaseCommand
from telegram import Update
from telegram.ext import Application, ContextTypes

from accounts.models import User
from core.logger import init_logger


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок для бота"""
    logging.exception("Error while handling an update: %s", context.error, exc_info=context.error)

    if not (update or isinstance(update, Update)):
        return

    if isinstance(context.error, User.DoesNotExist):
        logging.error(f"User with telegram_id {update.effective_user.id} not found")
        await update.effective_message.reply_text("Пользователь не найден. Пожалуйста, начните с команды /start.")

    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Извините, произошла ошибка обработки Вашего запроса. Попробуйте позже или начните сначала командой /start.",
        )
    except Exception as send_error:
        logging.error("Failed to send error message: %s", send_error)


class Command(BaseCommand):
    def handle(self, *args, **options):
        init_logger("bot")

        application = Application.builder().token(environ.get("TG_BOT_TOKEN")).build()

        for app_name in settings.INSTALLED_APPS:
            if app_name.startswith("django."):
                continue

            module_handlers = import_module(f"{app_name}.router").HANDLERS
            application.add_handlers(module_handlers)
            logging.info(f"Added {len(module_handlers)} handlers from {app_name}")

        application.add_error_handler(error_handler)

        application.run_polling()
