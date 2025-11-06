from custom_requester.custom_requester import CustomRequester
from constants import MOVIES_BASE_URL, MOVIES_ENDPOINT

class MoviesAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_movies(self, movi_get_params, expected_status=200):
        """ просмотр списка всех фильмов """
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=movi_get_params,
            expected_status=expected_status)

    def post_movies(self, movi_data, expected_status=201):
        """ создание фильма """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movi_data,
            expected_status=expected_status)

    def get_movies_by_id(self, movi_id, expected_status=200):
        """ получение фильма по id """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{movi_id}",
            expected_status=expected_status)

    def del_movies_by_id(self, movi_id, expected_status=200):
        """ удаление фильма по id """
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movi_id}",
            expected_status=expected_status)

    def patch_movies_by_id(self, movi_id, movi_data, expected_status=200):
        """ редактирование фильма по id """
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movi_id}",
            data=movi_data,
            expected_status=expected_status)
