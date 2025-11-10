from http.client import responses

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
def movie_data():
    random_film = DataGenerator.generate_random_movie()
    return random_film


@pytest.fixture(scope="function")
def movie_get_params():
    movie_get_params = DataGenerator.generate_random_movie_get_params()
    return movie_get_params

@pytest.fixture(scope="function")
def created_movie(api_manager):
    random_film = DataGenerator.generate_random_movie()
    response = api_manager.movies_api.post_movies(random_film, expected_status=201).json()
    yield response
    api_manager.movies_api.del_movies_by_id(response['id'])


@pytest.fixture(scope="function")
def created_movie_for_del(api_manager):
    random_film = DataGenerator.generate_random_movie()
    response = api_manager.movies_api.post_movies(random_film, expected_status=201).json()
    return response

@pytest.fixture(scope="session")
def admin_user():
    return {"email": "api1@gmail.com",
            "password": "asdqwe123Q"}
