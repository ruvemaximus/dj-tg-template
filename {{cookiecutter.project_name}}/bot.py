#!/usr/bin/env python

import logging
import os
from contextlib import suppress
from importlib import import_module

import django
from telegram.ext import Application

from core.logger import init_logger

with suppress(ImportError):
    from dotenv import load_dotenv

    load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg_bot.settings")
django.setup()

logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    init_logger("bot")

    application = Application.builder().token(os.getenv("TG_BOT_TOKEN")).build()

    for app_name in django.conf.settings.INSTALLED_APPS:
        if app_name.startswith("django."):
            continue

        application.add_handlers(import_module(f"{app_name}.router").HANDLERS)

    application.run_polling()


if __name__ == "__main__":
    main()
