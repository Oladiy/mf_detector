import logging
import os


DEFAULT_DEVICES_NOT_FOUND_MESSAGE = "Devices not found"
DEFAULT_GREETING = "Hello! Use command /help to get info"
DEFAULT_INFO_LANGUAGE = 'english'
DEFAULT_MONITORING_REJECT_MESSAGE = "The monitoring has already been started"
DEFAULT_REPORT_REJECT_MESSAGE = "Failed to get the report: the service status is 'monitoring'"

DEFAULT_TIMEOUT_SECONDS = 10

SUPPORTED_LANGUAGES = (
    'english',
    'russian'
)
SUPPORTED_DEVICES_DETECTOR_TYPES = (
    'PersonalAccountParser',
)

logger = logging.getLogger(__name__)


class ServiceParameters:
    def __init__(self):
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        assert self.telegram_bot_token, "Telegram bot token is not specified"

        self.devices_not_found_message = os.getenv('DEVICES_NOT_FOUND_MESSAGE', DEFAULT_DEVICES_NOT_FOUND_MESSAGE)
        self.greeting = os.getenv('GREETING', DEFAULT_GREETING)
        self.info_language = os.getenv('INFO_LANGUAGE', DEFAULT_INFO_LANGUAGE)
        self._check_info_language()
        self.monitoring_reject_message = os.getenv('MONITORING_REJECT_MESSAGE', DEFAULT_MONITORING_REJECT_MESSAGE)
        self.report_reject_message = os.getenv('REPORT_REJECT_MESSAGE', DEFAULT_REPORT_REJECT_MESSAGE)

        self.timeout = int(os.getenv('TIMEOUT', DEFAULT_TIMEOUT_SECONDS))
        assert self.timeout > 0, "The 'TIMEOUT' parameter must be a positive integer"

        self.devices_detector_type = os.getenv('DEVICES_DETECTOR_TYPE')
        assert self.devices_detector_type in SUPPORTED_DEVICES_DETECTOR_TYPES, \
            f"Supported devices detectors: {SUPPORTED_DEVICES_DETECTOR_TYPES}"

        self.service_status = 'stopped'
        self.previous_devices_info = None

    def _check_info_language(self):
        if self.info_language not in SUPPORTED_LANGUAGES:
            logger.warning(f"Language {self.info_language} is not supported yet :(\nUse English by default")
