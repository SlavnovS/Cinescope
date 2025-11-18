from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, USER_BASE_URL
from custom_requester.custom_requester import CustomRequester


class AuthAPI(CustomRequester):
    """ Класс для работы с аутентификацией. """
    def __init__(self, session):
        super().__init__(session=session, base_url=USER_BASE_URL)

    def register_user(self, user_data, expected_status=201):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status)

    def login_user(self, login_data, expected_status=201):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status)

    def authenticate(self, user_creds):
        response = self.login_user(user_creds)
        if "accessToken" not in response.json():
            raise KeyError("token is missing")
        token = response.json()["accessToken"]
        self._update_session_headers(authorization=f"Bearer {token}")
        return response