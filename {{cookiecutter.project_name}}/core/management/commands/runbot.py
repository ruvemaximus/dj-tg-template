import asyncio
import logging
from importlib import import_module

import uvicorn
from django.conf import settings
from django.core.management import BaseCommand
from telegram import Update
from telegram.ext import Application, ContextTypes

from accounts.models import User
from core.logger import init_logger
from core.utils import build_app


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

async def run_bot(application: Application):
    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app="tg_bot.asgi:application",
            port=settings.ADMIN_PORT,
            log_level=logging.INFO if settings.DEBUG else logging.WARNING,
            host="127.0.0.1" if settings.DEBUG else "0.0.0.0",
            use_colors=settings.DEBUG,
            lifespan="off",
        )
    )

    async with application:
        await application.updater.start_polling()
        await application.start()
        await webserver.serve()
        await application.updater.stop()
        await application.stop()


class Command(BaseCommand):
    def handle(self, *args, **options):
        init_logger("bot")

        application: Application = build_app()

        for app_name in settings.INSTALLED_APPS:
            if app_name.startswith("django."):
                continue

            try:
                module_handlers = import_module(f"{app_name}.router").HANDLERS
                application.add_handlers(module_handlers)
                logging.info(f"Added {len(module_handlers)} handlers from {app_name}")
            except ModuleNotFoundError:
                logging.warning(f"Module '{app_name}.router' not found")

        application.add_error_handler(error_handler)
        asyncio.run(run_bot(application))
