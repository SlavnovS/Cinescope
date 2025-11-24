from resources.user_creds import SuperAdminCreds
import requests
import pytest
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from entities.user import User
from constants import Roles
from models.base_models import TestUser
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from playwright.sync_api import Page
from example import Tools

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
def creation_user_data(test_user: TestUser):
    test_user.verified = True
    test_user.banned = False
    return test_user


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
        creation_user_data.email,
        creation_user_data.password,
        list(Roles.USER.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    response = common_user.api.auth_api.authenticate(common_user.creds).json()
    yield common_user
    # super_admin.api.user_api.delete_user(response['user']['id'])


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
def test_user() -> TestUser:
    """Генерация случайного пользователя для тестов"""
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email = random_email,
        fullName = random_name,
        password = random_password,
        passwordRepeat = random_password,
        roles = [Roles.USER.value]
    )


@pytest.fixture(scope="function")
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
def created_movie_for_del(super_admin):
    random_film = DataGenerator.generate_random_movie()
    response = super_admin.api.movies_api.post_movies(random_film, expected_status=201).json()
    return response


# @pytest.fixture(scope="session")
# def admin_user():
#     return {"email": SuperAdminCreds.USERNAME,
#             "password": SuperAdminCreds.PASSWORD}

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper


@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

DEFAULT_UI_TIMEOUT = 30000  # Пример значения таймаута

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)  # Установка таймаута по умолчанию
    yield context  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()  # Контекст закрывается после завершения теста

@pytest.fixture(scope="function")  # Страница создается для каждого теста
def page(context) -> Page:
    page = context.new_page()
    yield page  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    page.close()  # Страница закрывается после завершения теста
