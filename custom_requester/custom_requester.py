import json
import logging
import os
from pydantic import BaseModel
from constants import RED, GREEN, RESET


class CustomRequester:
    """
    Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
    """
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        # self.session.verify = False  # 🔥 FIDDLER FIX
        # self.session.proxies = {
        #     'http': 'http://127.0.0.1:8888',
        #     'https': 'http://127.0.0.1:8888'
        # }

    def send_request(self, method, endpoint, data=None, params=None,
                     expected_status=200, need_logging=True):
        url = f"{self.base_url}{endpoint}"
        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(exclude_unset=True)) # почему не model_dump ??
        response = self.session.request(method, url, json=data, params=params, headers=self.headers)
        if need_logging:
            self.log_request_and_response(response, expected_status)
        if response.status_code != expected_status and not response.ok:
            raise ValueError(f"Unexpected status code: {response.status_code}. "
                             f"Expected: {expected_status}")
        return response

    def _update_session_headers(self, **kwargs):
        """
        Обновление заголовков сессии.
        :param kwargs: Дополнительные заголовки.
        """
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)

    def log_request_and_response(self, response, expected_status):
        """
        Логирование запросов и ответов.
        :param response: Объект ответа requests.response.
        :param expected_status: Ожидаемый статус код
        """
        try:
            request = response.request
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body != '{}' else ''

            # Логируем запрос
            # self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info("\n%s", "=" * 40 + " REQUEST " + "=" * 40)
            # self.logger.info(
            #     f"{GREEN}{full_test_name}{RESET}\n"
            #     f"curl -X {request.method} '{request.url}' \\\n"
            #     f"{headers} \\\n"
            #     f"{body}"
            # )
            self.logger.info(
                "%s%s%s\ncurl -X %s '%s' \\\n%s \\\n%s",
                GREEN, full_test_name, RESET, request.method, request.url, headers, body
            )
            # Обрабатываем ответ
            response_status = response.status_code
            is_success = response.ok
            response_data = response.text

            # Логируем ответ
            # self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            self.logger.info("\n%s", "=" * 40 + " REQUEST " + "=" * 40)
            if expected_status != response.status_code and not is_success:
                if 500 <= response_status < 600:
                    self.logger.critical(
                        "SERVER ERROR %s for %s %s\nResponse: %s",
                        response_status, request.method, request.url, response_data,
                    )
                # self.logger.error(
                #     f"\tSTATUS_CODE: {RED}{response_status}{RESET}\n"
                #     f"\tDATA: {RED}{response_data}{RESET}"
                # )
                self.logger.error(
                    "\tSTATUS_CODE: %s%s%s\n"
                    "\tDATA: %s%s%s",
                    RED, response_status, RESET, RED, response_data, RESET
                )
            else:
                # self.logger.info(
                #     f"\tSTATUS_CODE: {GREEN}{response_status}{RESET}\n"
                #     f"\tDATA:\n{response_data}"
                # )
                self.logger.info(
                    "\tSTATUS_CODE: %s%s%s\n"
                    "\tDATA:\n%s",
                    GREEN, response_status, RESET, response_data
                )
            # self.logger.info(f"{'=' * 80}\n")
            self.logger.info("%s", "=" * 80)
        except Exception as e:
            # self.logger.error(f"\nLogging failed: {type(e)} - {e}")
            self.logger.error("\nLogging failed: %s - %s", type(e).__name__, e)
