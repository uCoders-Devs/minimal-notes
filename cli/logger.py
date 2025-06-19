import logging
import logging.handlers

from pathlib import Path

class ColorFormatter(logging.Formatter):
    """Formater con ANSI Colors"""

    grey      = "\x1b[38;20m"
    yellow    = "\x1b[33;20m"
    red       = "\x1b[31;20m"
    bold_red  = "\x1b[31;1m"
    reset     = "\x1b[0m"
    log_format= "[%(asctime)s][%(name)s][%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"
    FORMATS   = {
        logging.DEBUG:    grey    + log_format + reset,
        logging.INFO:     grey    + log_format + reset,
        logging.WARNING:  yellow  + log_format + reset,
        logging.ERROR:    red     + log_format + reset,
        logging.CRITICAL: bold_red+ log_format + reset,
    }


    def format(self, record):
        fmt = self.FORMATS.get(record.levelno)
        return logging.Formatter(fmt).format(record)


class PlainFormatter(logging.Formatter):
    """Formatter para el archivo de logging"""

    log_format = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"


    def format(self, record):
        return logging.Formatter(self.log_format).format(record)


class Logger:
    """Minimal Logger exportable con file handling y streaming opcional"""

    def __init__(self, logger_name: str, log_file: str = "latest.log", stream: bool = False, level: int = logging.DEBUG) -> None:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(level)
        self._logger.propagate = False
        self._logger.handlers.clear()

        fh = logging.handlers.RotatingFileHandler(
            filename=log_file,
            encoding='utf-8',
            maxBytes=32*1024*1024,
            backupCount=5
        )
        fh.setFormatter(PlainFormatter())
        self._logger.addHandler(fh)

        if stream:
            sh = logging.StreamHandler()
            sh.setFormatter(ColorFormatter())
            self._logger.addHandler(sh)


    def get(self) -> logging.Logger:
        return self._logger


if __name__ == "__main__":
    logger = Logger(log_file="data/latest.log", stream=True).get()
    logger.info("Esto es informacion")
    logger.debug("El logger funciona bien")
    logger.warning("Se van a ejecutar dos simulacros!")
    logger.error("Ocurrio un error! (SIMULACRO)")
    logger.critical("SE ELIMINO LA BASE DE DATOS! (SIMULACRO)")
