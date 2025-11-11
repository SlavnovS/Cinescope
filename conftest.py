from http.client import responses
from resources.user_creds import SuperAdminCreds
import requests
import pytest
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from entities.user import User
from constants import Roles

@pytest.fixture(scope="function")
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture(scope="function")
def creation_user_data(test_user: dict):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture(scope="function")
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.USER.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture(scope="session")
def session():
    """ Фикстура для создания HTTP-сессии. """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """ Фикстура для создания экземпляра ApiManager. """
    return ApiManager(session)

@pytest.fixture(scope="function")
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
        "roles": [Roles.USER.value]
    }

@pytest.fixture(scope="session")
def movie_data():
    random_film = DataGenerator.generate_random_movie()
    return random_film


@pytest.fixture(scope="function")
def movie_get_params():
    movie_get_params = DataGenerator.generate_random_movie_get_params()
    return movie_get_params

@pytest.fixture(scope="function")
def created_movie(super_admin):
    random_film = DataGenerator.generate_random_movie()
    response = super_admin.api.movies_api.post_movies(random_film, expected_status=201).json()
    yield response
    super_admin.api.movies_api.del_movies_by_id(response['id'])


@pytest.fixture(scope="function")
def created_movie_for_del(api_manager):
    random_film = DataGenerator.generate_random_movie()
    response = api_manager.movies_api.post_movies(random_film, expected_status=201).json()
    return response

@pytest.fixture(scope="session")
def admin_user():
    return {"email": "api1@gmail.com",
            "password": "asdqwe123Q"}
