from custom_requester.custom_requester import CustomRequester
from constants import PAYMENT_BASE_URL, PAYMENT_CREATE, PAYMENT_GET


class PaymentAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=PAYMENT_BASE_URL)

    def post_payment(self, data, expected_status=201):
        """Создание оплаты"""
        return self.send_request(
            method="POST",
            endpoint=PAYMENT_CREATE,
            data=data,
            expected_status=expected_status)

    def get_my_payments(self, expected_status=200):
        """Получение списка своих платежей"""
        return self.send_request(
            method="GET",
            endpoint=PAYMENT_GET,
            expected_status=expected_status
        )

    def get_payments_by_id(self, params, expected_status=200):
        """Получение списка платежей по ID"""
        return self.send_request(
            method="GET",
            endpoint=PAYMENT_GET + '/' + params,
            # params=params,
            expected_status=expected_status
        )

    def get_all_payments(self, params, expected_status=200):
        """Получение списка платежей по ID"""
        return self.send_request(
            method="GET",
            endpoint="find-all",
            params=params,
            expected_status=expected_status
        )
