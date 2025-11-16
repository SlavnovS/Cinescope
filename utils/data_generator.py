import random
import string
from faker import Faker
import datetime


faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        # выбирает 8 случайных элементов из строки = 26 букв + 10 цифр -> список -> джоин в строку
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    # Гадя Хренова

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        # all_chars — строка из букв (верхний и нижний регистр) + цифр + спецсимволов
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_movie():
        return {
            "name": f"The {faker.catch_phrase()}",
            "imageUrl": "https://avatars.mds.yandex.net/"
                        "i?id=cce8b15040c138004875a832069b6b47_l-5736044-images-thumbs&n=13",
            "price": random.choice([100, 600, 500, 250]),
            "description": faker.sentence(nb_words=5),
            "location": random.choice(["MSK", "SPB"]),
            "published": True,
            "genreId": 1
        }

    @staticmethod
    def generate_random_movie_get_params():
        return {'pageSize': random.randint(2, 4),
                'page': 1,
                'minPrice': random.randint(150, 280),
                'maxPrice': random.randint(300, 1000),
                'locations': random.choice(["MSK", "SPB"]),
                'published': 'true',
                'genreId': 1,
                'createdAt': random.choice(['asc', 'desc'])
                }

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_random_int(my_int: int):
        return random.randint(1, my_int)