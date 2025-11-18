from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import MoviesDataBaseCreds

USERNAME = MoviesDataBaseCreds.USERNAME
PASSWORD = MoviesDataBaseCreds.PASSWORD
HOST = MoviesDataBaseCreds.HOST
PORT = MoviesDataBaseCreds.PORT
DATABASE_NAME = MoviesDataBaseCreds.DATABASE_NAME

#  движок для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False  # Установить True для отладки SQL запросов
)

# создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()