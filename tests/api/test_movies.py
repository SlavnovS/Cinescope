class TestMovies:

    def test_get_movies(self, api_manager):
        """ Тест получения списка фильмов """
        api_manager.movies_api.get_movies()

    def test_get_movies_with_params(self, api_manager, movie_get_params):
        """ Тест получения списка фильмов """
        response = api_manager.movies_api.get_movies(movie_get_params).json()
        print(5)
        assert len(response['movies']) == movie_get_params['pageSize'], \
            'фильтр не отрабатывает, неверное количество фильмов на странице'
        for movie in response['movies']:
            assert movie_get_params['maxPrice'] > movie['price'] > movie_get_params['minPrice'], \
                'фильтр не отрабатывает, цена вне указанного диапазона'
            assert movie['location'] == movie_get_params['locations'], 'фильтр не отрабатывает, неправильная локация'

    def test_post_movies(self, super_admin, api_manager, movie_data):
        """ Тест поста нового фильма """
        json_response = super_admin.api.movies_api.post_movies(movie_data).json()
        movi_id = json_response['id']
        assert json_response["name"] == movie_data["name"], \
            "название фильма не соответствует отправленному"
        assert json_response["price"] == movie_data["price"], \
            "стоймость фильма не соответствует отправленному"
        api_manager.movies_api.get_movies_by_id(movi_id)

    def test_get_movies_by_id(self, api_manager, created_movie):
        """ Тест поиска фильма по ID. """
        movi_id = created_movie['id']
        response = api_manager.movies_api.get_movies_by_id(movi_id)
        assert response.json()["name"] == created_movie["name"], "не совпадает название фильма"
        assert response.json()["price"] == created_movie["price"], "не совпадает стоимость фильма"

    def test_patch_movies_by_id(self, api_manager, created_movie):
        """ Тест редактирования фильма по ID. """
        movie_data = {"name": 'Californication',
                      "price": 350}
        api_manager.movies_api.patch_movies_by_id(movi_id=created_movie['id'],
                                                  movi_data=movie_data)
        get_response = api_manager.movies_api.get_movies_by_id(created_movie['id'])
        assert get_response.json()["name"] == movie_data["name"], "не поменялось название фильма"
        assert get_response.json()["price"] == movie_data["price"], "не поменялась стоимость фильма"

    def test_del_movies_by_id(self, api_manager, created_movie_for_del):
        """ Тест удаления фильма по ID. """
        api_manager.movies_api.del_movies_by_id(created_movie_for_del['id'])
        get_response = api_manager.movies_api.get_movies_by_id(created_movie_for_del['id'],
                                                               expected_status=404)
        assert get_response.status_code == 404, "фильм не удалился"


class TestMoviesNegative:

    def test_negative_get_movies(self, api_manager, movie_get_params):
        """ Негативный тест получения списка фильмов """
        movie_get_params['locations'] = "Gdov"
        api_manager.movies_api.get_movies(movie_get_params,
                                          expected_status=400)

    # def test_negative_post_movies(self, api_manager, created_movie, super_admin):
    #     """ Негативный тест поста нового фильма """
    #     json_response = super_admin.api.movies_api.post_movies(movie_data, expected_status=409).json()
    #     movi_id = json_response['id']
    #     assert json_response["name"] == movie_data["name"], \
    #         "название фильма не соответствует отправленному"
    #     assert json_response["price"] == movie_data["price"], \
    #         "стоймость фильма не соответствует отправленному"
    #     api_manager.movies_api.get_movies_by_id(movi_id)

        response = api_manager.movies_api.post_movies(created_movie, expected_status=409)
        assert response.json()["message"] == "Фильм с таким названием уже существует", \
            "неверный вывод ошибки"

    def test_negative_del_movies_by_id(self, api_manager):
        """ Негативный тест удаления фильма по ID. """
        api_manager.movies_api.del_movies_by_id("aaa", expected_status=404)

    def test_negative_patch_movies_by_id(self, api_manager, created_movie):
        """ Негативный тест редактирования фильма по ID. """
        movie_data = {"location": "Gdov",
                      "price": 350}
        api_manager.movies_api.patch_movies_by_id(movi_id=created_movie['id'],
                                                  movi_data=movie_data,
                                                  expected_status=400)
        get_response = api_manager.movies_api.get_movies_by_id(created_movie['id'])
        assert get_response.json()["price"] != 350, "применелись допустимые изменения"
        assert get_response.json()["location"] != "Gdov", "применелись недопустимые изменения"

    def test_negative_get_movies_by_id(self, api_manager):
        """ Негативный тест поиска фильма по ID. """
        response = api_manager.movies_api.get_movies_by_id(99999,
                                                           expected_status=404)
        assert response.json()["message"] == "Фильм не найден", \
            "неверный вывод ошибки"
