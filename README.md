# mf_detector
A service that collects information about devices connected to a local network and sends it to a telegram bot.

## Development
The service is currently under development (see [here](https://github.com/Oladiy/mf_detector#to-do) if you are interested) and supports only zyxel routers.

## Configuration parameters
* `TELEGRAM_BOT_TOKEN` - **Required**.
* `TIMEOUT` - Waiting time in seconds between cycles when using the `/monitoring` command. The default value is 10.
* `DEVICES_DETECTOR_TYPE` - Type of device detector. Currently, only personal account parsing is supported (`PersonalAccountParser`). **Required**.
* `LOG_LEVEL_STDOUT` - Logging level. The default value is 'INFO'.

When using the detector type PersonalAccountParser:
* `ROUTER_NAME` - The brand of the router. Currently only `zyxel` is supported. **Required**.
* `RDHCP_MF_URL` - URL of the HTML page with information about devices. **Required**.
* `URL_TO_LOGIN` - URL of the authorization page. **Required**.
* `BODY_TO_LOGIN` - The body of the POST request to login. **Required**.
* `TIMEOUT_TO_LOGIN` - Waiting time in seconds after re-logging in. The default value is 5.

Configuring messages (instead of default):
* `DEVICES_NOT_FOUND_MESSAGE` - The message that is displayed when there are no connected devices.
* `GREETING` - when using the `/start` command.
* `INFO_LANGUAGE` - So far it supports only `russian` and `english`. The default value is `english`.
* `MONITORING_REJECT_MESSAGE` - Error message when using the `/monitoring` command.
* `REPORT_REJECT_MESSAGE` - Error message when using the `/report` command. 


## Run
Export the required parameters and start the service:
```shell
./detector/start.py
```


## To do
* Add multiple languages support (a separate class).
* Add docstrings.
* Different routers support (to parse PA).
* Make normal HTML parsing (PersonalAccountHTMLParser).
* Add a parameter to skip lan interfaces.
* Add authorization to the telegram bot.
* Add a README in Russian.
* Add asynchronous service status update when monitoring mode is stopped.