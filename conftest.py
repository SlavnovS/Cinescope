import requests
import pytest
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager


@pytest.fixture(scope="session")
def test_user():
    """Генерация случайного пользователя для тестов"""
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture(scope="session")
def movi_data():
    random_film = DataGenerator.generate_random_movi()
    return random_film


@pytest.fixture(scope="session")
def movi_get_params():
    movi_get_params = DataGenerator.generate_random_movi_get_params()
    return movi_get_params


@pytest.fixture(scope="session")
def admin_user():
    return {"email": "api1@gmail.com",
            "password": "asdqwe123Q"}
