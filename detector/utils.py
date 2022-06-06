import logging


logger = logging.getLogger(__name__)

LOG_LEVELS = (
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',
)


def check_log_level(log_level: str):
    """Check the logger level based on the default list"""
    assert log_level in LOG_LEVELS, f"Valid 'LOG_LEVEL_STDOUT' values: {LOG_LEVELS}"
