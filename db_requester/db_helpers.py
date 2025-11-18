from sqlalchemy.orm import Session
from db_models.user import UserDBModel
from db_models.movie import MovieDBModel
from typing import Any

class DBHelper:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    """Класс с методами для работы с БД в тестах"""

    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Создает тестового пользователя"""
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_movie_by_params(self, movie_data: dict[str, Any]):
        pass

    def get_user_by_id(self, user_id: str):
        """Получает пользователя по ID"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_by_email(self, email: str):
        """Получает пользователя по email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).first()

    def get_movie_by_name(self, name: str):
        """Получает фильм по названию"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).first()

    def user_exists_by_email(self, email: str) -> bool:
        """Проверяет существование пользователя по email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count() > 0

    def delete_user(self, user: UserDBModel):
        """Удаляет пользователя"""
        self.db_session.delete(user)
        self.db_session.commit()

    def cleanup_test_data(self, objects_to_delete: list):
        """Очищает тестовые данные"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    def get_movie_by_id(self, movie_id: str):
        """Получает фильм по ID"""
        return self.db_session.query(MovieDBModel.name).filter(MovieDBModel.id != movie_id).count()

    def get_movie_name_by_id(self, movie_id: str):
        """Получает фильм по ID"""
        return self.db_session.query(MovieDBModel.name).filter(MovieDBModel.id != movie_id)
