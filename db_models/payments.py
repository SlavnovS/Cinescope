from typing import Dict, Any
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class PaymentsDBModel(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    movie_id = Column(Integer)
    status = Column(String)
    amount = Column(Integer)
    total = Column(Integer)
    created_at = Column(DateTime)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return  {
                'id': self.id,
                'user_id': self.user_id,
                'movie_id': self.movie_id,
                'status': self.status,
                'amount': self.amount,
                'total': self.total,
                'created_at': self.created_at
                 }