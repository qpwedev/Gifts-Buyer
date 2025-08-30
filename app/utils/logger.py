import datetime
import logging
import sys

SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


class SimpleFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        record.levelname = f"[{timestamp}] - [{record.levelname}]: "
        return super().format(record)


class CustomLogger(logging.Logger):
    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(SUCCESS_LEVEL):
            self._log(SUCCESS_LEVEL, msg, args, **kwargs)


logging.setLoggerClass(CustomLogger)
logger = logging.getLogger("gifts_buyer")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(SimpleFormatter('%(levelname)s %(message)s'))
logger.addHandler(handler)


def info(message: str) -> None:
    print("\r", end="")
    logger.info(message)


def warn(message: str) -> None:
    print("\r", end="")
    logger.warning(message)


def error(message: str) -> None:
    print("\r", end="")
    logger.error(message)


def success(message: str) -> None:
    print("\r", end="")
    if isinstance(logger, CustomLogger):
        logger.success(message)
    else:
        logger.info(f"[SUCCESS] {message}")


def log_same_line(message: str, level: str = "INFO") -> None:
    timestamp = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
    print(f"\r[{timestamp}] - [{level.upper()}]: {message}", end="", flush=True)
