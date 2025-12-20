import copy
import allure
import pytest
from api.api_manager import ApiManager
from models.base_models import RegisterUserResponse
from utils.data_generator import DataGenerator

skip_status = False

@allure.epic("cinescope")
@allure.feature("Тестирование API")
@allure.story("Позитивное тестирование TestAuthAPI")
class TestAuthAPI:


    @pytest.mark.smoke
    @allure.title("Тест регистрации пользователя")
    @allure.description("Тест проверяет регистрацию пользователя")
    def test_register_user(self, api_manager: ApiManager, test_user, super_admin):
        """ Тест на регистрацию пользователя. """
        response = api_manager.auth_api.register_user(user_data=test_user).json()
        response_data = RegisterUserResponse(**response)
        assert response_data.email == test_user.email, "Email не совпадает"
        super_admin.api.user_api.delete_user(response.get('id'))

    @pytest.mark.smoke
    @allure.title("Тест регистрации и авторизации пользователя")
    @allure.description("Тест проверяет регистрацию и авторизацию пользователя, наличие "
                        "получения токена при авторизации")
    def test_login_user(self, api_manager, test_user):
        """ Тест на регистрацию и авторизацию пользователя. """
        api_manager.auth_api.register_user(test_user).json()
        login_data = {"email": test_user.email,
                      "password": test_user.password}
        response = api_manager.auth_api.login_user(login_data).json()
        assert "accessToken" in response, "Токен доступа отсутствует в ответе"
        assert response["user"]["email"] == test_user.email, "Email не совпадает"



class TestNegativeAuthAPI:


    @pytest.mark.regression
    @allure.title("Негативный тест регистрации пользователя")
    @allure.description("Тест проверяет регистрацию пользователя с неверным passwordRepeat")
    def test_negative_register_user(self, api_manager: ApiManager, test_user):
        """ Негативный тест на регистрацию пользователя. """
        test_user.passwordRepeat = test_user.passwordRepeat[:8] + "45"
        response = api_manager.auth_api.register_user(test_user, expected_status=400)
        assert response.status_code == 400, "нет ошибки аутентификации"
        assert "accessToken" not in response.json(), "Токен доступа присутствует в ответе"

    @pytest.mark.regression
    @allure.title("Негативный тест регистрации и авторизации пользователя")
    @allure.description("Тест проверяет авторизацию пользователя с неверным паролем, отсутствие "
                        "получения токена при авторизации")
    def test_negative_login_user(self, api_manager, test_user):
        """ Негативный тест на регистрацию и авторизацию пользователя. """
        api_manager.auth_api.register_user(user_data=test_user)
        test_negative_user = test_user.model_copy()
        test_negative_user.password = test_negative_user.password[:8] + "45"
        response = api_manager.auth_api.login_user(test_negative_user, expected_status=401)
        assert "accessToken" not in response.json(), "Токен доступа присутствует в ответе"
        # а можно и так еще
        # response = api_manager.auth_api.login_user(test_user, expected_status=401)
        # assert "accessToken" not in response.json(), "Токен доступа присутствует в ответе"

@allure.epic("cinescope")
@allure.feature("Тестирование API")
@allure.story("Позитивное тестирование TestUser")
class TestUser:

    @pytest.mark.smoke
    @allure.title("Тест на создание пользователя")
    @allure.description("Тест проверяет создание пользователя администратором сайта, соответствие "
                        "данных пользователя, введенным параметрам")
    def test_create_user(self, super_admin, creation_user_data):
        """ Тест на создание пользователя. """
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        assert response.get('id'), "ID должен быть не пустым"  # вроде так достаточно
        assert response.get('email') == creation_user_data.email
        assert response.get('fullName') == creation_user_data.fullName
        assert response.get('roles', []) == creation_user_data.roles
        assert response.get('verified') is True

    @pytest.mark.smoke
    @allure.title("Тест на поиск пользователя по ID при наличии прав администратора")
    @allure.description("Тест проверяет поиск пользователя по ID администратором сайта, соответствие "
                        "данных пользователя, введенным параметрам")
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """ Тест на получение информации пользователя по ID с правами суперадмина. """
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data.email).json()
        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id'), "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data.email
        assert response_by_id.get('fullName') == creation_user_data.fullName
        assert response_by_id.get('roles', []) == creation_user_data.roles
        assert response_by_id.get('verified') is True

    @pytest.mark.smoke
    @pytest.mark.slow
    @allure.title("Тест на поиск пользователя по ID при отсутствии прав администратора")
    @allure.description("Тест проверяет невозможность поиска пользователя по ID при отсутствии прав администратора")
    def test_get_user_by_locator_common_user(self, common_user):
        """ Тест на получение информации пользователя по ID с правами юзера. """
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

    @pytest.mark.smoke
    @allure.title("Тест на удаление пользователя по ID при наличии прав администратора")
    @allure.description("Тест проверяет возможность удаления пользователя по ID администратором сайта")
    def test_delete_user(self, super_admin, creation_user_data):
        """ Тест на удаление пользователя по ID с правами суперадмина. """
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        super_admin.api.user_api.delete_user(response.get('id'))
        get_response = super_admin.api.user_api.get_user(response.get('id'))
        assert len(get_response.json()) == 0, "данные не удалились"

    @pytest.mark.regression
    @pytest.mark.skipif(skip_status, reason="Временно отключён")
    @allure.title("Тест на удаление пользователя по ID при отсутствии прав администратора")
    @allure.description("Тест проверяет невозможность удаления пользователя по ID при отсутствии прав администратора сайта")
    def test_delete_user_by_id_common_user(self, api_manager, super_admin, common_user):
        """ Тест на удаление пользователя по ID с правами юзера. """
        response_common_user = super_admin.api.user_api.get_user(common_user.email).json()
        post_user = copy.deepcopy(response_common_user)
        post_user["email"] = DataGenerator.generate_random_email()
        post_user["password"] = DataGenerator.generate_random_password()
        del post_user["id"]
        response = super_admin.api.user_api.create_user(post_user).json()
        api_manager.user_api.delete_user(response.get('id'), expected_status=401)
        common_user.api.user_api.delete_user(response.get('id'), expected_status=403)
        get_response = super_admin.api.user_api.get_user(response.get('id'))
        assert len(get_response.json()) != 0, "данные удалились"
        super_admin.api.user_api.delete_user(response.get('id'))


class TestUserDB:


    def test_create_user_db(self, super_admin, creation_user_data, db_helper):
        db_response = db_helper.get_user_by_email(creation_user_data.email)
        assert db_response is None
        response = super_admin.api.user_api.create_user(creation_user_data).json()
        db_response = db_helper.get_user_by_id(response['id'])
        assert db_response



