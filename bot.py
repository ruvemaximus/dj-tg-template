#!/usr/bin/env python

import logging
import os
from importlib import import_module

import django
from dotenv import load_dotenv
from telegram.ext import Application

from core.logger import init_logger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg_bot.settings")
django.setup()

logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    load_dotenv()
    init_logger("bot")

    application = Application.builder().token(os.getenv("TG_BOT_TOKEN")).build()

    for app_name in django.conf.settings.INSTALLED_APPS:
        if app_name.startswith("django."):
            continue

        application.add_handlers(import_module(f"{app_name}.router").HANDLERS)

    application.run_polling()


if __name__ == "__main__":
    main()
