from sqlalchemy import Column, String

from janeiro.plugins.database import ResourceEntity


class AccountEntity(ResourceEntity):
    __tablename__ = "accounts"

    username = Column(String(30), unique=True, index=True)
    email = Column(String(50), unique=True)
    password = Column(String, nullable=False)
