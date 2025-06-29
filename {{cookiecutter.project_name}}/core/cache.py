import logging

from django.conf import settings


def use_file_cache(filepath: str):
    """Отправка файла из кэша"""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            if hasattr(func, "_file_id"):
                await func(*args, **kwargs, media=func._file_id)
                return

            logging.info(f"File '{filepath}' not found in cache. Uploading to telegram...")
            with open(settings.BASE_DIR / filepath, "rb") as media_file:
                func._file_id = await func(*args, **kwargs, media=media_file)

        return wrapper

    return decorator
