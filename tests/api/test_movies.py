from pytest_check import check
import allure
import pytest
from datetime import datetime
import json

# pytestmark = pytest.mark.skip(reason="TASK-1234: Тесты временно отключены из-за нестабильности")
@allure.epic("cinescope")
@allure.feature("Тестирование API")
@allure.story("Позитивное тестирование MoviesAPI")
class TestMovies:

    @pytest.mark.smoke
    @allure.title("Тест получения списка фильмов")
    @allure.description("Тест проверяет получение списка фильмов")
    def test_get_movies(self, api_manager):
        """ Тест получения списка фильмов """
        api_manager.movies_api.get_movies()

    @pytest.mark.regression
    @allure.title("Тест получения списка фильмов по параметрам")
    @allure.description("Тест проверяет получение списка фильмов по "
                        "параметрам и соответствие ответа с введенными параметрами")
    def test_get_movies_with_params(self, api_manager, movie_get_params):
        """ Тест получения списка фильмов """
        response = api_manager.movies_api.get_movies(movie_get_params).json()
        assert len(response['movies']) == movie_get_params['pageSize'], \
            'фильтр не отрабатывает, неверное количество фильмов на странице'
        for movie in response['movies']:
            assert movie_get_params['maxPrice'] > movie['price'] > movie_get_params['minPrice'], \
                'фильтр не отрабатывает, цена вне указанного диапазона'
            assert movie['location'] == movie_get_params['locations'], 'фильтр не отрабатывает, неправильная локация'

    @allure.title("Тест получения списка фильмов с параметризацией")
    @allure.description("Тест проверяет получение списка фильмов по параметрам "
                        "используя параметризацию пайтеста")
    @pytest.mark.parametrize("maxPrice,minPrice,locations,genreld", [(750, 400, 'MSK', 1), (500, 200, 'SPB', 5), ],
                             ids=["750-400, MSK, 1 movie", "500-200, SPB, 5 movie"])
    def test_get_movies_with_parametrize_params(self, api_manager, maxPrice, minPrice, locations, genreld):
        """ Тест получения списка фильмов """
        response = api_manager.movies_api.get_movies(
            {'maxPrice': maxPrice, 'minPrice': minPrice, 'locations': locations,
             'genreld': genreld, 'pageSize': 5}).json()
        for movie in response['movies']:
            assert maxPrice > movie['price'] > minPrice, \
                'фильтр не отрабатывает, цена вне указанного диапазона'
            assert movie['location'] == locations, 'фильтр не отрабатывает, неправильная локация'

    @pytest.mark.smoke
    @allure.title("Тест поста нового фильма")
    @allure.description("Тест проверяет пост нового фильма, получение нового фильма по GET запросу,"
                        "соответствие названия и стоимости фильма отправленному в POST")
    def test_post_movies(self, super_admin, api_manager, movie_data):
        """ Тест поста нового фильма"""
        json_response = super_admin.api.movies_api.post_movies(movie_data).json()
        movi_id = json_response['id']
        assert json_response["name"] == movie_data["name"], \
            "название фильма не соответствует отправленному"
        assert json_response["price"] == movie_data["price"], \
            "стоймость фильма не соответствует отправленному"
        api_manager.movies_api.get_movies_by_id(movi_id)
        super_admin.api.movies_api.del_movies_by_id(movi_id)

    @pytest.mark.smoke
    @pytest.mark.slow
    @allure.title("Тест запроса фильма по ID")
    @allure.description("Тест проверяет возможность запросить фильм по ID и соответствие "
                        "ожидаемого и действительного результатов")
    def test_get_movies_by_id(self, api_manager, created_movie):
        """ Тест поиска фильма по ID. """
        movi_id = created_movie['id']
        response = api_manager.movies_api.get_movies_by_id(movi_id)
        assert response.json()["name"] == created_movie["name"], "не совпадает название фильма"
        assert response.json()["price"] == created_movie["price"], "не совпадает стоимость фильма"

    @pytest.mark.slow
    @allure.title("Тест изменения фильма по ID")
    @allure.description("Тест проверяет возможность изменить фильм по ID и применяемость изменений")
    def test_patch_movies_by_id(self, super_admin, api_manager, created_movie):
        """ Тест редактирования фильма по ID. """
        movie_data = {"name": 'Californication',
                      "price": 350}
        super_admin.api.movies_api.patch_movies_by_id(movi_id=created_movie['id'],
                                                      movi_data=movie_data)
        get_response = api_manager.movies_api.get_movies_by_id(created_movie['id'])
        assert get_response.json()["name"] == movie_data["name"], "не поменялось название фильма"
        assert get_response.json()["price"] == movie_data["price"], "не поменялась стоимость фильма"

    @pytest.mark.regression
    @allure.title("Тест удаления фильма по ID")
    @allure.description("Тест проверяет возможность удалить фильм по ID")
    def test_del_movies_by_id(self, super_admin, api_manager, created_movie_for_del):
        """ Тест удаления фильма по ID. """
        super_admin.api.movies_api.del_movies_by_id(created_movie_for_del['id'])
        get_response = api_manager.movies_api.get_movies_by_id(created_movie_for_del['id'], expected_status=404)
        assert get_response.status_code == 404, "фильм не удалился"


@allure.epic("cinescope")
@allure.feature("Тестирование API")
@allure.story("Негативное тестирование MoviesAOI")
class TestMoviesNegative:

    @pytest.mark.regression
    @allure.title("Негативный тест получения списка фильмов по параметрам")
    @allure.description("Тест проверяет невозможность получения списка фильмов по невалидным параметрам")
    def test_negative_get_movies(self, api_manager, movie_get_params):
        """ Негативный тест получения списка фильмов """
        movie_get_params['locations'] = "Gdov"
        api_manager.movies_api.get_movies(movie_get_params, expected_status=400)

    @pytest.mark.regression
    @pytest.mark.slow
    @allure.title("Негативный тест поста нового фильма")
    @allure.description("Тест проверяет невозможность повторного занесения существующего фильма")
    def test_negative_post_movies(self, api_manager, created_movie, super_admin):
        """ Негативный тест поста нового фильма """
        response = super_admin.api.movies_api.post_movies(created_movie, expected_status=409)
        assert response.json()["message"] == "Фильм с таким названием уже существует", \
            "неверный вывод ошибки"

    @pytest.mark.regression
    @allure.title("Негативный тест запроса фильма по ID")
    @allure.description("Тест проверяет невозможность запросить фильм по не существующему ID")
    def test_negative_get_movies_by_id(self, api_manager):
        """ Негативный тест поиска фильма по ID. """
        response = api_manager.movies_api.get_movies_by_id(99999, expected_status=404)
        assert response.json()["message"] == "Фильм не найден", "неверный вывод ошибки"

    @pytest.mark.regression
    @pytest.mark.slow
    @allure.title("Негативный тест изменения фильма по ID")
    @allure.description("Тест проверяет невозможность изменить фильм по ID с некорректными параметрами")
    def test_negative_patch_movies_by_id(self, super_admin, api_manager, created_movie):
        """ Негативный тест редактирования фильма по ID. """
        movie_data = {"location": "Gdov",
                      "price": 350}
        super_admin.api.movies_api.patch_movies_by_id(movi_id=created_movie['id'],
                                                      movi_data=movie_data,
                                                      expected_status=400)
        get_response = api_manager.movies_api.get_movies_by_id(created_movie['id'])
        assert get_response.json()["price"] != 350, "применелись допустимые изменения"
        assert get_response.json()["location"] != "Gdov", "применелись недопустимые изменения"

    @pytest.mark.regression
    @allure.title("Негативный тест удаления фильма по ID")
    @allure.description("Тест проверяет статус код при удалении фильма по несуществующему ID или при отсутствии прав")
    def test_negative_del_movies_by_id(self, common_user, super_admin, created_movie):
        """ Негативный тест удаления фильма по ID. """
        super_admin.api.movies_api.del_movies_by_id("aaa", expected_status=404)
        common_user.api.movies_api.del_movies_by_id(created_movie["id"], expected_status=403)


@allure.epic("cinescope")
@allure.feature("Тестирование API")
@allure.story("Позитивное тестирование MoviesAPI с проверкой работы БД")
class TestMoviesDB:

    @pytest.mark.regression
    @allure.title("Проверка поста фильма в БД")
    @allure.description("Тест проверяет что при посте фильма он появляется в БД, после удаления - удаляется из БД")
    def test_post_movies_db(self, super_admin, api_manager, movie_data, db_helper):
        """ Тест поста нового фильма с проверкой работы БД"""
        assert not db_helper.get_movie_by_name(movie_data['name']), "такой фильм есть в БД"
        json_response = super_admin.api.movies_api.post_movies(movie_data).json()
        movi_id = json_response['id']
        assert db_helper.get_movie_by_id(movi_id), "фильм не добавился в БД"
        assert json_response["name"] == movie_data["name"], \
            "название фильма не соответствует отправленному"
        assert json_response["price"] == movie_data["price"], \
            "стоймость фильма не соответствует отправленному"
        assert api_manager.movies_api.get_movies_by_id(movi_id), "фильм не получить через GET"
        super_admin.api.movies_api.del_movies_by_id(movi_id)
        assert not db_helper.get_movie_by_id(movi_id), "фильм не удалился из БД"

    @pytest.mark.slow
    @allure.title("Тест изменения фильма по ID")
    @allure.description("Тест проверяет возможность изменить фильм по ID и применяемость изменений")
    def test_patch_movies_by_id_db(self, super_admin, api_manager, created_movie, db_helper):
        """ Тест редактирования фильма по ID. """
        with allure.step("Проверяю что фильм есть в БД"):
            assert db_helper.get_movie_by_id(created_movie["id"]), "фильма нет в БД"
            movie_data = {"name": 'Californication',
                          "price": 350}
        with allure.step("Меняю название и стоимость фильма"):
            super_admin.api.movies_api.patch_movies_by_id(movi_id=created_movie['id'],
                                                          movi_data=movie_data)
        get_response = api_manager.movies_api.get_movies_by_id(created_movie['id'])
        response_db = db_helper.get_movie_by_id(created_movie["id"])
        with allure.step("проверяю соответствие изменения введенным параметрам"):
            with check:
                msg = "Имя фильма не совпадает с ожидаемым"
                check.equal(response_db.name, movie_data["name"], msg)
                check.equal(get_response.json()["name"], movie_data["name"], "не поменялось название фильма")
                check.equal(get_response.json()["price"], movie_data["price"], "не поменялась стоимость фильма")

    @pytest.mark.regression
    @allure.title("Тест соответствия get запроса базе данных")
    @allure.description("Тест проверяет что в ответе на get запрос информация совпадает с базой данных")
    def test_get_movies_by_id_db(self, super_admin, db_helper, created_movie):
        response = super_admin.api.movies_api.get_movies_by_id(created_movie['id']).json()
        response_bd = db_helper.get_movie_by_name(created_movie['name'])
        with check:
            check.equal(response_bd.id, response['id'], "Не соответствуют ID фильмов")
            check.equal(response_bd.name, response['name'], "Не соответствуют названия фильмов")
            check.equal(response_bd.price, response['price'], "Не соответствуют стоимости фильмов")
            check.equal(response_bd.published, response['published'], "Не соответствуют опубликованности фильмов")
            check.equal(response_bd.genre_id, response['genreId'], "Не соответствуют жанры фильмов")

    # @pytest.mark.flaky(reruns=2, reruns_delay=1)
    @pytest.mark.regression
    @allure.title("Тест поиска фильмов по параметрам в соответствии с БД")
    @allure.description("Тест проверяет соответствие результата API поиска фильмов "
                        "по параметрам с результатом поиска в базе данных")
    def test_get_movies_with_params_db(self, api_manager, movie_get_params, db_helper):
        response = api_manager.movies_api.get_movies(movie_get_params).json()
        response_db = db_helper.get_movie_by_params(movie_get_params)
        print(response)
        print(response_db)
        assert len(response['movies']) == len(response_db) == movie_get_params['pageSize'], \
            'фильтр не отрабатывает, неверное количество фильмов на странице'
        for i in range(len(response['movies'])):
            assert response_db[i].name == response['movies'][i]['name'], \
                "API ответ не соответствует ответу из базы данных"
            assert response_db[i].id == response['movies'][i]['id'], "API ответ не соответствует ответу из базы данных"
            assert response_db[i].price == response['movies'][i]['price'], \
                "API ответ не соответствует ответу из базы данных"
            assert movie_get_params['minPrice'] < response_db[i].price < movie_get_params['maxPrice'], \
                'фильтр не отрабатывает, цена вне указанного диапазона'
            assert response_db[i].location == response['movies'][i]['location'] == movie_get_params['locations'], \
                'фильтр не отрабатывает, неправильная локация'


@pytest.mark.kafka
class TestKafkaPaymentAPI:
    def test_api_sends_to_kafka(self, super_admin, creeds_payment, kafka_consumer):
        super_admin.api.payment_api.post_payment(data=creeds_payment, expected_status=201)

        # Читаем сообщение из Kafka
        # messages = list(kafka_consumer)
        # my_messages = messages[:1]
        # print(messages)
        # print(my_messages)

    @pytest.mark.parametrize("page,page_size,status,created_at",[(1, 5, "SUCCESS", 'desc'),
                                                                (1, 2, "INVALID_CARD", 'desc')])
    def test_get_all_payments(self, super_admin, page, page_size, status, created_at):  # 2 отдельных теста
        response = super_admin.api.payment_api.get_all_payments({'page':page,
                                                                 'pageSize':page_size,
                                                                 'status':status,
                                                                 'created_at':created_at}).json()
        with allure.step('проверка соответствия вывода параметрам'):
            with check:
                check.equal(response.get('page'), page, "несоответствие номера страницы")
                check.equal(response.get('pageSize'), page_size, "несоответствие позиций на странице")
            for i in response.get("payments"):
                assert i['status'] == status, "статус не соответствует"
            if created_at == "asc":
                dates = [datetime.fromisoformat(i['createdAt'].replace('Z', '+00:00'))
                         for i in response.get("payments")]
                assert all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))
            else:
                dates = [datetime.fromisoformat(i['createdAt'].replace('Z', '+00:00'))
                         for i in response.get("payments")]
                assert all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1))

    def test_get_payments_by_id(self, super_admin):
        user_id = '0bfbe544-2f80-472f-af9b-b7986490a3d7'
        response = super_admin.api.payment_api.get_payments_by_id(params=user_id).json()

        # print(json.dumps(response, indent=2))
        for i in response:
            assert i.get('userId') == user_id

    def test_get_my_payments(self, common_user, creeds_payment):
        common_user.api.payment_api.post_payment(data=creeds_payment).json()
        common_id = common_user.api.auth_api.login_user({"email": common_user.email,
                      "password": common_user.password}).json()['user']['id']
        response = common_user.api.payment_api.get_my_payments().json()
        for i in response:
            assert i.get('userId') == common_id


    # def test_olo(self, db_helper):
    #     db_response = db_helper.get_movie_by_name("Список Шиндлера")
    #     id_movie = db_response.to_dict()["id"]
    #     print(f"AAAAAAAAAAAAAAAAAAA{db_response}")
    #
    # def test_get_movie_name_by_id(self, db_helper):
    #     db_response = db_helper.get_movie_by_id('11')
    #     print(f"AAAAAAAAAAAAAAAAAAAAA{db_response}")
