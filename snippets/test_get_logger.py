import pytest

import logging
import warnings
from io import StringIO
from get_logger import get_logger


@pytest.mark.parametrize(
    "logger_name, logger_message_level",
    [
        ("test_logger", "INFO"),
        ("another_logger", "DEBUG"),
        ("", "WARNING"),
        ("", "error"),
        ("", ""),
    ],
)
def test_get_logger_with_valid_args(logger_name, logger_message_level):
    # Act
    logger = get_logger(logger_name, logger_message_level)

    # Assert
    # validate logger_name
    assert isinstance(logger, logging.Logger)
    if logger_name != "":
        assert logger.name == logger_name
    else:
        assert logger.name == "root"

    # validate logger_message_level
    if logger_message_level == "":
        assert logger.level == logging.getLevelName("DEBUG")
    elif isinstance(logger_message_level, str):
        assert logger.level == logging.getLevelName(logger_message_level.upper())
    else:
        assert logger.level == logging.getLevelName(logger_message_level)


@pytest.mark.parametrize(
    "logger_name, logger_message_level",
    [
        ("test_logger", "INVALID"),
        ("test_logger", "asdg"),
        ("test_logger", "dsf"),
        ("test_logger", "a"),
    ],
)
def test_get_logger_with_invalid_level(logger_name, logger_message_level):
    # Act
    with warnings.catch_warnings(record=True) as w:
        logger = get_logger(logger_name, logger_message_level)

    # Assert
    assert len(w) == 1
    assert issubclass(w[-1].category, UserWarning)
    assert f"Invalid logger level {logger_message_level}" in str(w[-1].message)
    assert logger.level == logging.DEBUG


def test_get_logger_with_logging_output():
    # Arrange
    logger_name = "test_logger"
    logger_message_level = "INFO"
    stream = StringIO()
    ch = logging.StreamHandler(stream)
    logger = get_logger(logger_name, logger_message_level)
    logger.addHandler(ch)

    # Act
    logger.info("Test message")

    # Assert
    assert "Test message" in stream.getvalue()


def test_get_logger_with_file_output():
    # Arrange
    logger_name = "test_logger"
    logger_message_level = "INFO"
    logger = get_logger(logger_name, logger_message_level, save_logfile=True)

    # Act
    logger.info("Test message")

    # Assert
    with open(f"{logger_name}.log", "r") as f:
        assert "Test message" in f.read()
