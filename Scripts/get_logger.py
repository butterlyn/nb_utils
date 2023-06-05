# %%
# IMPORTS 

import logging
import warnings

# %%
# GLOBAL VARIABLES


# %%
# HELPER FUNCTIONS


def _validate_logger_level(logger_message_level):
    valid_logger_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if not any(level in logger_message_level.upper() for level in valid_logger_levels):
        warnings.warn(
            f"Invalid logger level {logger_message_level}. Must be one of {valid_logger_levels}. Setting level to DEBUG."
        )
        logger_message_level = "DEBUG"
    return logger_message_level.upper()


def _create_formatter():
    return logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s - %(message)s"
    )


def _create_console_handler(logger_message_level, formatter):
    ch = logging.StreamHandler()
    ch.setLevel(logging.getLevelName(logger_message_level))
    ch.setFormatter(formatter)
    return ch


def _create_file_handler(logger_name, logger_message_level, formatter):
    fh = logging.FileHandler(f"{logger_name}.log")
    fh.setLevel(logging.getLevelName(logger_message_level))
    fh.setFormatter(formatter)
    return fh


# %%
# COMPOSABLE FUNCTIONS


def get_logger(
    logger_name: str = __name__,
    logger_message_level: str = "DEBUG",
    save_logfile: bool = False,
) -> logging.Logger:
    # validate logger_message_level
    logger_message_level = _validate_logger_level(logger_message_level)

    # initialise logger from logging
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.getLevelName(logger_message_level))

    # create formatter
    formatter = _create_formatter()

    # create console handler and set level to debug
    ch = _create_console_handler(logger_message_level, formatter)
    logger.addHandler(ch)

    # create file handler
    if save_logfile:
        fh = _create_file_handler(logger_name, logger_message_level, formatter)
        logger.addHandler(fh)

    return logger


# %%
# MODULE-LEVEL FUNCTION(S)

# N/A

# %%
# MAIN

if __name__ == "__main__":
    pass
    # N/A package only module
