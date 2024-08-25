import logging


class CustomFormatter(logging.Formatter):
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"

    def __format_factory(color: str):
        return f"%(asctime)s {color}[%(levelname)s]\033[0m [%(name)s] %(message)s"

    FORMATS = {
        logging.DEBUG: __format_factory(RESET),
        logging.INFO: __format_factory(CYAN),
        logging.WARNING: __format_factory(YELLOW),
        logging.ERROR: __format_factory(RED),
        logging.CRITICAL: __format_factory(RED),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.DEBUG])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def init_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    console_handler.setLevel(level=level)
    logger.addHandler(console_handler)

    logging.basicConfig(
        level=level,
        handlers=[console_handler],
    )

    return logger
