from sqlalchemy import Column, Integer, String

from janeiro.plugins.database import Entity


class AccountEntity(Entity):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False)
    name = Column(String(30), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
