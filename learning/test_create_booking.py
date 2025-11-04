import pytest
from constants import BASE_URL

class TestBookings:
    booking_id = None
    request_body = None
    def test_create_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"
        booking_id = create_booking.json().get("bookingid")

        TestBookings.booking_id = booking_id # добавляю для кода ниже
        TestBookings.request_body = create_booking.request.body # добавляю для кода ниже

        print(create_booking.request.body) # для сравнения

        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # # Удаляем бронирование
        # deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        # assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # # Проверяем, что бронирование больше недоступно
        # get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        # assert get_booking.status_code == 404, "Бронь не удалилась"

    def test_put_booking(self, auth_session, booking_data):
        put_booking = auth_session.put(f"{BASE_URL}/booking/{TestBookings.booking_id}",
                                       json=booking_data)
        assert put_booking.status_code == 200, "Ошибка обновления брони"

        print(put_booking.request.body) # для сравнения

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{TestBookings.booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        booking_json = get_booking.json()
        assert booking_json["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"
        # проверяем что изменились данные бронирования
        assert TestBookings.request_body != get_booking.json(), "не поменялись данные"
        TestBookings.request_body = booking_json #берем тело ответа для проверки PATCH

    def test_patch_booking(self, auth_session):
        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{TestBookings.booking_id}",
                                           json={"firstname": "Sanek",
                                                 "lastname": "Saneek"})
        assert patch_booking.status_code == 200, "Ошибка корректировки брони"
        get_booking = auth_session.get(f"{BASE_URL}/booking/{TestBookings.booking_id}")
        assert TestBookings.request_body != get_booking.json, "не поменялось"

        print(get_booking.json())

    def test_negativ_create_booking(self, auth_session, booking_data):
        negativ_create_booking = auth_session.post(f"{BASE_URL}/booking",
                                                   json=booking_data.pop("lastname"))
        assert negativ_create_booking.status_code != 200, "ресурс создан без обязательного поля"

        negativ_create_booking = auth_session.post(f"{BASE_URL}/booking",
                                                   json=booking_data.update({"totalprice":"ggg"}))
        assert negativ_create_booking.status_code != 200, "ресурс создан с неверным типом данных"

    def test_negativ_put_patch(self, auth_session, booking_data):
        test_negativ_put = auth_session.put(f"{BASE_URL}/booking/9999999999999",
                                            json=booking_data)
        assert test_negativ_put.status_code != 200, "обновлен не существующий ресурс"
        print(TestBookings.booking_id)

        test_negativ_patch = auth_session.patch(f"{BASE_URL}/booking/{TestBookings.booking_id}",
                                                json="")
        assert test_negativ_patch.status_code != 200, "ресурс обновлен без данных"

