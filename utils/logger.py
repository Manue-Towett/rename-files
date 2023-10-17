import logging
from typing import Optional

class Logger:
    """Logs info, warning and error messages"""
    def __init__(self, name: Optional[str]=None) -> None:
        if name is None:
            name = __class__.__name__

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        self.__set_up_handlers()

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warn(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message, exc_info=True)

    def __set_up_handlers(self) -> None:
        s_handler = logging.StreamHandler()
        f_handler = logging.FileHandler("./logs/logs.log", 
                                        mode="w")

        s_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)

        fmt = logging.Formatter(
            "%(name)s:%(levelname)s - %(message)s")

        s_handler.setFormatter(fmt)
        f_handler.setFormatter(fmt)

        self.logger.addHandler(s_handler)
        self.logger.addHandler(f_handler)