"""
Enhanced logging configuration for Sales Coach AI
Provides structured logging with rotation, levels, and production-ready features
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional


class CustomFormatter(logging.Formatter):
    """
    Custom formatter with color coding for console output
    """

    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors for console"""
        # Add color to levelname for console
        if hasattr(self, 'use_color') and self.use_color:
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"

        return super().format(record)


def setup_logger(
    name: str = 'sales_coach',
    level: Optional[str] = None,
    log_dir: Optional[str] = None,
    console_level: Optional[str] = None,
    file_level: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    use_color: bool = True
) -> logging.Logger:
    """
    Setup and configure logger with console and file handlers

    Args:
        name: Logger name
        level: Default logging level (overrides all if set)
        log_dir: Directory for log files (default: ../logs)
        console_level: Console output level (default: INFO)
        file_level: File output level (default: DEBUG)
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        use_color: Use colored output in console

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)

    # Determine log level from environment or parameters
    if level is None:
        level = os.getenv('LOG_LEVEL', 'INFO')

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create logs directory
    if log_dir is None:
        log_dir = os.getenv('LOGS_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs'))

    os.makedirs(log_dir, exist_ok=True)

    # Determine handler levels
    if console_level is None:
        console_level = os.getenv('CONSOLE_LOG_LEVEL', 'INFO')
    if file_level is None:
        file_level = os.getenv('FILE_LOG_LEVEL', 'DEBUG')

    # ================================================================
    # CONSOLE HANDLER (Colored output for development)
    # ================================================================

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, console_level.upper(), logging.INFO))

    # Use color formatter for console
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    if use_color and sys.stdout.isatty():
        console_format = CustomFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_format.use_color = True

    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # ================================================================
    # FILE HANDLER (Detailed logs with rotation)
    # ================================================================

    # Daily log file
    log_filename = os.path.join(log_dir, f'sales_coach_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(getattr(logging, file_level.upper(), logging.DEBUG))

    # Detailed format for file logs
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # ================================================================
    # ERROR FILE HANDLER (Critical errors only)
    # ================================================================

    error_filename = os.path.join(log_dir, 'errors.log')
    error_handler = RotatingFileHandler(
        error_filename,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)

    # Add detailed error format with exception info
    error_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s\n'
        'File: %(pathname)s:%(lineno)d\n'
        'Function: %(funcName)s()\n'
        'Message: %(message)s\n'
        '%(exc_info)s\n' + '=' * 80,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    error_handler.setFormatter(error_format)
    logger.addHandler(error_handler)

    # ================================================================
    # PERFORMANCE LOG HANDLER (Optional - for timing metrics)
    # ================================================================

    if os.getenv('ENABLE_PERFORMANCE_LOGGING', 'false').lower() == 'true':
        perf_filename = os.path.join(log_dir, 'performance.log')
        perf_handler = TimedRotatingFileHandler(
            perf_filename,
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        perf_handler.setLevel(logging.INFO)
        perf_format = logging.Formatter(
            '%(asctime)s,%(message)s',  # CSV format for easy parsing
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        perf_handler.setFormatter(perf_format)

        # Create performance logger
        perf_logger = logging.getLogger(f'{name}.performance')
        perf_logger.setLevel(logging.INFO)
        perf_logger.addHandler(perf_handler)
        perf_logger.propagate = False

    # Don't propagate to root logger
    logger.propagate = False

    return logger


def get_performance_logger(name: str = 'sales_coach') -> logging.Logger:
    """Get or create performance logger for timing metrics"""
    return logging.getLogger(f'{name}.performance')


# ================================================================
# CONTEXT MANAGER FOR PERFORMANCE LOGGING
# ================================================================

import time
from contextlib import contextmanager
from typing import Generator


@contextmanager
def log_performance(operation: str, logger: Optional[logging.Logger] = None) -> Generator[None, None, None]:
    """
    Context manager to log operation performance

    Usage:
        with log_performance('api_call'):
            # your code here
            result = expensive_operation()

    Args:
        operation: Name of the operation being measured
        logger: Logger to use (default: performance logger)
    """
    if logger is None:
        logger = get_performance_logger()

    start_time = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        logger.info(f'{operation},{elapsed:.4f}')


# ================================================================
# CUSTOM LOG LEVELS (Optional)
# ================================================================

# Add custom TRACE level below DEBUG
TRACE = 5
logging.addLevelName(TRACE, 'TRACE')


def trace(self, message, *args, **kwargs):
    """Log trace-level message"""
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kwargs)


logging.Logger.trace = trace


# ================================================================
# UTILITY FUNCTIONS
# ================================================================

def log_exception(logger: logging.Logger, message: str, exc: Exception) -> None:
    """
    Log exception with full traceback

    Args:
        logger: Logger instance
        message: Custom message
        exc: Exception to log
    """
    logger.error(f"{message}: {str(exc)}", exc_info=True)


def sanitize_sensitive_data(data: dict, sensitive_keys: list = None) -> dict:
    """
    Remove sensitive data from dict before logging

    Args:
        data: Dictionary potentially containing sensitive data
        sensitive_keys: List of keys to redact (default: common sensitive keys)

    Returns:
        Sanitized dictionary
    """
    if sensitive_keys is None:
        sensitive_keys = [
            'password', 'api_key', 'secret', 'token', 'auth',
            'credit_card', 'ssn', 'api-key', 'api_token'
        ]

    sanitized = data.copy()
    for key in sanitized:
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            sanitized[key] = '***REDACTED***'

    return sanitized
