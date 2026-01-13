from pytest_check import check
import allure
import pytest
from datetime import datetime, timedelta
import json
from models.base_models import PaymentsList, PaymentGetResponse


@pytest.mark.kafka
class TestKafkaPaymentAPI:
    def test_api_sends_to_kafka(self, super_admin, creeds_payment, db_helper, common_user, kafka_consumer):
        # super_admin.api.payment_api.post_payment(data=creeds_payment, expected_status=201)
        common_user.api.payment_api.post_payment(data=creeds_payment, expected_status=201).json()
        common_id = common_user.api.auth_api.login_user({"email": common_user.email,
                                                         "password": common_user.password}
                                                         ).json()['user']['id']
        db_new_payment = db_helper.get_payment_by_user_id_and_movie_id(id=creeds_payment['movieId'],
                                                          u_id=common_id).to_dict().values()
        with allure.step('сравнение с БД'):
            assert common_id in db_new_payment
            assert creeds_payment['movieId'] in db_new_payment
            assert creeds_payment['amount'] in db_new_payment

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

    def test_get_payments_by_id(self, super_admin, db_helper):
        user_id = '0bfbe544-2f80-472f-af9b-b7986490a3d7'
        response = super_admin.api.payment_api.get_payments_by_id(params=user_id)
        payments_in_response = [PaymentGetResponse(**i) for i in response.json()]
        for i in payments_in_response:
            assert i.user_id == user_id
        db_response = db_helper.get_payment_by_user_id(user_id)
        assert len(db_response) == len(payments_in_response), 'длинна ответа не совпадает с БД'
        for i, j in zip(db_response, payments_in_response):
            assert i.id == j.id, 'id не совпадают'
            assert i.user_id == j.user_id, 'user_id не совпадают'
            assert i.movie_id == j.movie_id, 'movie_id не совпадают'
            assert i.status == j.status, 'status не совпадают'
            assert i.amount == j.amount, 'amount не совпадают'
            assert i.total == j.total, 'total не совпадают'
            assert i.created_at == j.created_at.replace(tzinfo=None), 'created_at не совпадают'

    def test_get_my_payments(self, common_user, creeds_payment, db_helper):
        with allure.step('пост фильма'):
            common_user.api.payment_api.post_payment(data=creeds_payment).json()
        with allure.step('достаем id пользователя'):
            common_id = common_user.api.auth_api.login_user({"email": common_user.email,
                      "password": common_user.password}).json()['user']['id']
        with allure.step('запрос на поиск своих платежей и валидация ответа'):
            response = common_user.api.payment_api.get_my_payments().json()
            response_list_of_models = [PaymentGetResponse.model_validate(i) for i in response]
        with allure.step('проверка соответствия запроса с id'):
            for i in response_list_of_models:
                assert i.user_id == common_id
        with allure.step('проверка интеграции с БД'):
            payments = db_helper.get_payment_by_user_id(common_id)
            assert payments[0].user_id == common_id, 'id не совпали'
