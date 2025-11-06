class TestMovies:
    movi_id = None

    def test_get_movies(self, api_manager, movi_get_params):
        """ Тест получения списка фильмов """
        response = api_manager.movies_api.get_movies(movi_get_params)

    def test_negative_get_movies(self, api_manager, movi_get_params):
        """ Негативный тест получения списка фильмов """
        negative_movi_get_params = movi_get_params.copy()
        negative_movi_get_params['locations'] = "Gdov"
        response = api_manager.movies_api.get_movies(negative_movi_get_params,
                                                     expected_status=400)

    def test_post_movies(self, api_manager, movi_data):
        """ Тест поста нового фильма """
        response = api_manager.movies_api.post_movies(movi_data)
        TestMovies.movi_id = response.json()['id']
        assert response.json()["name"] == movi_data["name"], \
            "название фильма не соответствует отправленному"
        assert response.json()["price"] == movi_data["price"], \
            "стоймость фильма не соответствует отправленному"

    def test_negative_post_movies(self, api_manager, movi_data):
        """ Негативный тест поста нового фильма """
        response = api_manager.movies_api.post_movies(movi_data, expected_status=409)
        assert response.json()["message"] == "Фильм с таким названием уже существует", \
            "неверный вывод ошибки"

    def test_get_movies_by_id(self, api_manager, movi_data):
        """ Тест поиска фильма по ID. Ищем фильм, который создали """
        response = api_manager.movies_api.get_movies_by_id(TestMovies.movi_id)
        assert response.json()["name"] == movi_data["name"], "не совпадает название фильма"
        assert response.json()["price"] == movi_data["price"], "не совпадает стоимость фильма"

    def test_negative_get_movies_by_id(self, api_manager):
        """ Негативный тест поиска фильма по ID. Ищем фильм, который создали """
        response = api_manager.movies_api.get_movies_by_id(99999,
                                                           expected_status=404)
        assert response.json()["message"] == "Фильм не найден", \
            "неверный вывод ошибки"

    def test_patch_movies_by_id(self, api_manager):
        """ Тест редактирования фильма по ID. Редактируем фильм, который создали """
        movi_data = {"name": "Californication",
                     "price": 350}
        response = api_manager.movies_api.patch_movies_by_id(movi_id=TestMovies.movi_id,
                                                             movi_data=movi_data)
        get_response = api_manager.movies_api.get_movies_by_id(TestMovies.movi_id)
        assert get_response.json()["name"] == "Californication", "не поменялось название фильма"
        assert get_response.json()["price"] == 350, "не поменялась стоимость фильма"

    def test_negative_patch_movies_by_id(self, api_manager):
        """ Негативный тест редактирования фильма по ID. Редактируем фильм, который создали """
        movi_data = {"location": "Gdov",
                     "price": 350}
        response = api_manager.movies_api.patch_movies_by_id(movi_id=TestMovies.movi_id,
                                                             movi_data=movi_data,
                                                           expected_status=400)
        get_response = api_manager.movies_api.get_movies_by_id(TestMovies.movi_id)
        assert get_response.json()["price"] == 350, "не применелись допустимые изменения"
        assert get_response.json()["location"] != "Gdov", "применелись недопустимые изменения"

    def test_del_movies_by_id(self, api_manager):
        """ Тест удаления фильма по ID. Удаляем фильм, который создали """
        response = api_manager.movies_api.del_movies_by_id(TestMovies.movi_id)
        get_response = api_manager.movies_api.get_movies_by_id(TestMovies.movi_id,
                                                               expected_status=404)
        assert get_response.status_code == 404, "фильм не удалился"

    def test_negative_del_movies_by_id(self, api_manager):
        """ Негативный тест удаления фильма по ID. Удаляем фильм, который создали """
        response = api_manager.movies_api.del_movies_by_id("aaa",
                                                           expected_status=404)

