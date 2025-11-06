from api.api_manager import ApiManager


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

    def test_negative_register_user(self, api_manager: ApiManager, test_user):
        """ Негативный тест на регистрацию пользователя. """
        del test_user["passwordRepeat"]
        response = api_manager.auth_api.register_user(test_user, expected_status=400)
        assert response.status_code == 400, "нет ошибки аутентификации"
        assert "accessToken" not in response.json(), "Токен доступа присутствует в ответе"

    def test_login_user(self, api_manager, test_user):
        """ Тест на регистрацию и авторизацию пользователя. """
        response = api_manager.auth_api.login_user(test_user)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == test_user["email"], "Email не совпадает"

    def test_negative_login_user(self, api_manager, test_user):
        """ Негативный тест на регистрацию и авторизацию пользователя. """
        test_negative_user = test_user.copy()
        test_negative_user["password"] = test_user["password"] + "asd"
        response = api_manager.auth_api.login_user(test_negative_user, expected_status=401)
        assert "accessToken" not in response.json(), "Токен доступа присутствует в ответе"

    # токен созданного пользователя подгружаю в хеддеры
    # не уверен что функция login_user вообще нужна, но оставил так
    def test_authenticate_user(self, api_manager, test_user):
        """ Логинимся под обычным юзером и обновляем токен """
        response = api_manager.auth_api.authenticate(test_user)

    def test_negative_get_user_info(self, api_manager):
        """ Негативный тест на получение информации о пользователе по ID. """
        response = api_manager.user_api.get_user_info(TestAuthAPI.user_id, expected_status=403)
        assert response.json() == {'error': 'Forbidden', 'message': 'Forbidden resource',
                                   'statusCode': 403}, "неверное тело ответа"

    def test_negative_delete_user(self, api_manager):
        """ Негативный тест на удаление пользователя по ID. """
        if TestAuthAPI.user_id[:1] != '4': # ну это прям совсем затычка - мне самому не нравится
            negative_user_id = '4' + TestAuthAPI.user_id[1:]
        else:
            negative_user_id = '5' + TestAuthAPI.user_id[1:]
        response = api_manager.user_api.delete_user(negative_user_id, expected_status=403)
        assert response.json() == {'message': 'Forbidden', 'statusCode': 403},\
            "неверное тело ответа"

    # только тут вхожу под админом и добавляю токен в хеддеры
    # думаю ты скажешь что это можно сделать более правильно =)
    def test_admin_login(self, api_manager, admin_user):
        """ Логинимся под админом и обновляем токен """
        response = api_manager.auth_api.authenticate(admin_user)

    def test_get_user_info(self, api_manager):
        """ Тест на получение информации о пользователе по ID. """
        response = api_manager.user_api.get_user_info(TestAuthAPI.user_id)
        response_data = response.json()
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_delete_user(self, api_manager):
        """ Тест на удаление пользователя по ID. """
        response = api_manager.user_api.delete_user(TestAuthAPI.user_id)
        get_responce = api_manager.user_api.get_user_info(TestAuthAPI.user_id)
        assert len(get_responce.json()) == 0, "данные не удалились"


