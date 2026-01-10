"""utils.py"""

from os import getenv

from telegram.ext import Application


def build_app(need_updater=True) -> Application:
    if not need_updater:
        return Application.builder().updater(None).token(getenv("TG_BOT_TOKEN")).build()
    return Application.builder().token(getenv("TG_BOT_TOKEN")).build()
