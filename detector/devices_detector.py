import logging
import os
import requests
import time

from personal_account_html_parser import PersonalAccountHTMLParser
from service_parameters import ServiceParameters


DEFAULT_TIMEOUT_TO_LOGIN_SECONDS = 5

logger = logging.getLogger(__name__)

SUPPORTED_ROUTERS = (
    'zyxel',
)


class DevicesDetector:
    def __init__(self, service_parameters: ServiceParameters):
        self.devices_detector_type = service_parameters.devices_detector_type

        if self.devices_detector_type == 'PersonalAccountParser':
            self.router_name = os.getenv('ROUTER_NAME')
            assert self.router_name in SUPPORTED_ROUTERS, f"Supported routers: {SUPPORTED_ROUTERS}"
            self.rdhcp_mf_url = os.getenv('RDHCP_MF_URL')
            assert self.rdhcp_mf_url, "RDHCP MF URL is required to get info about connected devices"

            self.url_to_login = os.getenv('URL_TO_LOGIN')
            self.body_to_login = os.getenv('BODY_TO_LOGIN')
            self.timeout_to_login = int(os.getenv('TIMEOUT_TO_LOGIN', DEFAULT_TIMEOUT_TO_LOGIN_SECONDS))
            assert self.timeout_to_login > 0, "The 'TIMEOUT_TO_LOGIN' parameter must be a positive integer"

            self.pa_html_parser = PersonalAccountHTMLParser()
            self.pa_html_parser.set_parser(self.router_name)

    def get_devices_info(self) -> str:
        if self.devices_detector_type == 'PersonalAccountParser':
            return self.personal_account_parser()

    def personal_account_parser(self) -> str:
        if self.router_name == 'zyxel':
            return self.zyxel_pa_parser()

    def zyxel_pa_parser(self) -> str:
        while True:
            try:
                # login
                requests.post(self.url_to_login, data=self.body_to_login)
                response = requests.get(self.rdhcp_mf_url)
                self.pa_html_parser.feed(response.text)
                return ''.join(self.pa_html_parser.retrieve_devices())
            except Exception as exc:
                logger.error(exc)
                # login and repeat after timeout
                requests.post(self.url_to_login, data=self.body_to_login)
                time.sleep(self.timeout_to_login)
