from http.client import responses

from api.api_manager import ApiManager
from conftest import admin_user, common_user


class TestAuthAPI:
    user_id = None

    def test_register_user(self, api_manager: ApiManager, test_user):
        """ Тест на регистрацию пользователя. """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"
        TestAuthAPI.user_id = response_data["id"]

    def test_login_user(self, api_manager, test_user):
        """ Тест на регистрацию и авторизацию пользователя. """
        api_manager.auth_api.register_user(test_user).json()
        login_data = {"email": test_user["email"],
                      "password": test_user["password"]}
        response = api_manager.auth_api.login_user(login_data).json()
        assert "accessToken" in response, "Токен доступа отсутствует в ответе"
        assert response["user"]["email"] == test_user["email"], "Email не совпадает"


class TestNegativeAuthAPI:

    def test_negative_register_user(self, api_manager: ApiManager, test_user):
        """ Негативный тест на регистрацию пользователя. """
        del test_user["passwordRepeat"]
        response = api_manager.auth_api.register_user(test_user, expected_status=400)
        assert response.status_code == 400, "нет ошибки аутентификации"
        assert "accessToken" not in response.json(), "Токен доступа присутствует в ответе"

    def test_negative_login_user(self, api_manager, test_user):
        """ Негативный тест на регистрацию и авторизацию пользователя. """
        test_negative_user = test_user.copy()
        test_negative_user["password"] = test_user["password"] + "asd"
        response = api_manager.auth_api.login_user(test_negative_user, expected_status=401)
        assert "accessToken" not in response.json(), "Токен доступа присутствует в ответе"


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        """ Тест на создание пользователя по ID с правами суперадмина. """
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        # assert response.get('id') and response['id'] != '', "ID должен быть не пустым" - зачем??

        assert response.get('id'), "ID должен быть не пустым"  # вроде так достаточно
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """ Тест на получение информации пользователя по ID с правами суперадмина. """
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id'), "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True

    def test_get_user_by_id_common_user(self, common_user):
        """ Тест на получение информации пользователя по ID с правами юзера. """
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

    def test_delete_user(self, super_admin, creation_user_data):
        """ Тест на удаление пользователя по ID с правами суперадмина. """
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        super_admin.api.user_api.delete_user(response.get('id'))
        get_response = super_admin.api.user_api.get_user(response.get('id'))
        assert len(get_response.json()) == 0, "данные не удалились"

    def test_delete_user_by_id_common_user(self, common_user, super_admin, creation_user_data):
        """ Тест на удаление пользователя по ID с правами юзера. """
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        common_user.api.user_api.delete_user(response.get('id'), expected_status=403)
        get_response = super_admin.api.user_api.get_user(response.get('id'))
        assert len(get_response.json()) != 0, "данные удалились"
        super_admin.api.user_api.delete_user(response.get('id'))
