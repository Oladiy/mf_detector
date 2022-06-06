#!/usr/bin/env python3
import logging
import os
import telebot
import time

from devices_detector import DevicesDetector
from log import init_log
from service_parameters import ServiceParameters
from utils import check_log_level


DEFAULT_LOG_LEVEL_STDOUT = 'INFO'

logger = logging.getLogger(__name__)


def main():
    log_level_stdout = os.getenv('LOG_LEVEL_STDOUT', DEFAULT_LOG_LEVEL_STDOUT)
    check_log_level(log_level_stdout)
    init_log(log_level_stdout)

    service_parameters = ServiceParameters()

    devices_detector = DevicesDetector(service_parameters)
    bot = telebot.TeleBot(service_parameters.telegram_bot_token, parse_mode=None)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        logger.info(f"Attempt to start chat: {message}")
        bot.reply_to(message, service_parameters.greeting)

    @bot.message_handler(commands=['help'])
    def send_help(message):
        logger.info(f"Attempt to get help: {message}")
        # TODO replace with speficic class
        if service_parameters.info_language == 'english':
            info = [
                "/monitoring - start monitoring with a specified period\n",
                "/stop - stop monitoring\n",
                "/report - display the current situation\n",
            ]
        else:
            info = [
                "/monitoring - начать наблюдение с заданным периодом\n",
                "/stop - остановить наблюдение\n",
                "/report - отобразить текущую ситуацию\n",
            ]
        bot.reply_to(message, ''.join(info))

    @bot.message_handler(commands=['stop'])
    def stop(message):
        logger.info(f"Attempt to stop the monitoring: {message}")
        # TODO add different languages support
        # NOTE think about async
        if service_parameters.service_status == 'monitoring':
            service_parameters.service_status = 'stopped'
            result = "The monitoring is stopped"
            service_parameters.previous_devices_info = None
        else:
            result = "The monitoring is already stopped"
        bot.reply_to(message, result)

    @bot.message_handler(commands=['monitoring'])
    def monitoring(message):
        logger.info(f"Attempt to start a monitoring: {message}")
        if service_parameters.service_status == 'monitoring':
            logger.warning("Failed attempt to start monitoring: it has already been started")
            bot.reply_to(message, service_parameters.monitoring_reject_message)
            return

        service_parameters.service_status = 'monitoring'
        while True:
            try:
                if service_parameters.service_status == 'stopped':
                    logger.info("Stopping the monitoring")
                    break
                devices_info = devices_detector.get_devices_info()
                if not devices_info and service_parameters.previous_devices_info:
                    service_parameters.previous_devices_info = devices_info
                    bot.reply_to(message, service_parameters.devices_not_found_message)
                elif not service_parameters.previous_devices_info == devices_info:
                    service_parameters.previous_devices_info = devices_info
                    bot.reply_to(message, devices_info)
                time.sleep(service_parameters.timeout)
            except Exception as exc:
                logger.error(exc)

    @bot.message_handler(commands=['report'])
    def report(message):
        logger.info(f"Attempt to get a report: {message}")
        if service_parameters.service_status == 'monitoring':
            logger.warning("Failed attempt to get a report: the service status is 'monitoring'")
            bot.reply_to(message, service_parameters.report_reject_message)
        else:
            devices_info = devices_detector.get_devices_info()
            if not devices_info:
                bot.reply_to(message, service_parameters.devices_not_found_message)
            else:
                bot.reply_to(message, devices_info)

    @bot.message_handler(func=lambda m: True)
    def echo_all(message):
        send_welcome(message)

    bot.infinity_polling()


if __name__ == '__main__':
    main()
