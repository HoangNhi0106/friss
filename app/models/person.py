from sqlalchemy import Column, String, DateTime, Integer
from app.db.database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    birthday = Column(DateTime, nullable=True)
    identification = Column(String, nullable=True)