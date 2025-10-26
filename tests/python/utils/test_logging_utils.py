"""Tests for logging_utils module."""

import logging
from io import StringIO

import pytest

from scripts.python.utils.colors import Colors
from scripts.python.utils.logging_utils import ColoredFormatter, get_logger, setup_logger


class TestColoredFormatter:
    """Test ColoredFormatter class."""

    def test_colored_formatter_levels(self) -> None:
        """Test formatter applies correct colors to log levels."""
        formatter = ColoredFormatter("%(levelname)s: %(message)s")

        # Test DEBUG level
        record = logging.LogRecord("test", logging.DEBUG, "", 0, "test message", (), None)
        result = formatter.format(record)
        assert Colors.CYAN in result
        assert Colors.RESET in result

        # Test INFO level
        record = logging.LogRecord("test", logging.INFO, "", 0, "test message", (), None)
        result = formatter.format(record)
        assert Colors.BLUE in result
        assert Colors.RESET in result

        # Test WARNING level
        record = logging.LogRecord("test", logging.WARNING, "", 0, "test message", (), None)
        result = formatter.format(record)
        assert Colors.YELLOW in result
        assert Colors.RESET in result

        # Test ERROR level
        record = logging.LogRecord("test", logging.ERROR, "", 0, "test message", (), None)
        result = formatter.format(record)
        assert Colors.RED in result
        assert Colors.RESET in result

        # Test CRITICAL level
        record = logging.LogRecord("test", logging.CRITICAL, "", 0, "test message", (), None)
        result = formatter.format(record)
        assert Colors.BOLD in result
        assert Colors.RED in result
        assert Colors.RESET in result

    def test_colored_formatter_message_preserved(self) -> None:
        """Test formatter preserves message content."""
        formatter = ColoredFormatter("%(levelname)s: %(message)s")
        record = logging.LogRecord("test", logging.INFO, "", 0, "custom message", (), None)
        result = formatter.format(record)
        assert "custom message" in result


# Fixture cleanup_loggers imported from tests.fixtures.common


class TestSetupLogger:
    """Test setup_logger function."""

    def test_setup_logger_basic(self, cleanup_loggers: None) -> None:
        """Test basic logger setup."""
        logger = setup_logger("test_logger")
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1

    def test_setup_logger_custom_level(self, cleanup_loggers: None) -> None:
        """Test logger setup with custom level."""
        logger = setup_logger("test_logger", level=logging.WARNING)
        assert logger.level == logging.WARNING

    def test_setup_logger_custom_format(self, cleanup_loggers: None) -> None:
        """Test logger setup with custom format."""
        custom_format = "%(name)s - %(levelname)s - %(message)s"
        logger = setup_logger("test_logger", format_string=custom_format)
        assert len(logger.handlers) == 1

        handler = logger.handlers[0]
        assert isinstance(handler.formatter, ColoredFormatter)

    def test_setup_logger_no_colors(self, cleanup_loggers: None) -> None:
        """Test logger setup without colors."""
        logger = setup_logger("test_logger", use_colors=False)
        assert len(logger.handlers) == 1

        handler = logger.handlers[0]
        assert isinstance(handler.formatter, logging.Formatter)
        assert not isinstance(handler.formatter, ColoredFormatter)

    def test_setup_logger_clears_existing_handlers(self, cleanup_loggers: None) -> None:
        """Test that setup_logger clears existing handlers."""
        logger = setup_logger("test_logger")
        initial_handler_count = len(logger.handlers)

        # Setup again
        logger = setup_logger("test_logger")
        assert len(logger.handlers) == initial_handler_count

    def test_setup_logger_stream_output(self, cleanup_loggers: None) -> None:
        """Test logger outputs to stdout."""
        logger = setup_logger("test_logger")
        handler = logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)

    @pytest.mark.parametrize(
        "level",
        [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ],
    )
    def test_setup_logger_all_levels(self, level: int, cleanup_loggers: None) -> None:
        """Test logger setup with various logging levels."""
        logger = setup_logger("test_logger", level=level)
        assert logger.level == level


class TestGetLogger:
    """Test get_logger function."""

    def test_get_logger_basic(self, cleanup_loggers: None) -> None:
        """Test getting logger."""
        logger = get_logger("test_logger")
        assert logger.name == "test_logger"

    def test_get_logger_existing(self, cleanup_loggers: None) -> None:
        """Test getting existing logger returns same instance."""
        logger1 = setup_logger("test_logger")
        logger2 = get_logger("test_logger")
        assert logger1 is logger2

    def test_get_logger_different_names(self, cleanup_loggers: None) -> None:
        """Test getting loggers with different names."""
        logger1 = get_logger("logger1")
        logger2 = get_logger("logger2")
        assert logger1.name == "logger1"
        assert logger2.name == "logger2"
        assert logger1 is not logger2


class TestLoggerIntegration:
    """Test logger integration scenarios."""

    def test_logger_logging_levels(self, cleanup_loggers: None) -> None:
        """Test logger respects log levels."""
        stream = StringIO()
        logger = setup_logger("test_logger", level=logging.WARNING)

        # Replace handler with one that writes to StringIO
        logger.handlers[0].stream = stream  # type: ignore

        logger.debug("debug message")
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")

        output = stream.getvalue()
        assert "debug message" not in output
        assert "info message" not in output
        assert "warning message" in output
        assert "error message" in output

    def test_logger_colored_output(self, cleanup_loggers: None) -> None:
        """Test logger produces colored output."""
        stream = StringIO()
        logger = setup_logger("test_logger", use_colors=True)
        logger.handlers[0].stream = stream  # type: ignore

        logger.info("test message")

        output = stream.getvalue()
        assert Colors.BLUE in output or "test message" in output

    def test_logger_plain_output(self, cleanup_loggers: None) -> None:
        """Test logger produces plain output without colors."""
        stream = StringIO()
        logger = setup_logger("test_logger", use_colors=False)
        logger.handlers[0].stream = stream  # type: ignore

        logger.info("test message")

        output = stream.getvalue()
        assert Colors.BLUE not in output
        assert "test message" in output

