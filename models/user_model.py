from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings

class UserModel(settings.DBBaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=True)
    lastname = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=True, unique=True)
    password = Column(String(256), nullable=True)
    is_admin = Column(Boolean, default=False)
    articles = relationship(
        "ArticleModel",
        back_populates="creator",
        cascade="all, delete-orphan",
        uselist=True,
        lazy="joined"
    )
    