from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base

from models.base import Base
from libs.config import get_config
from libs.database_controller import get_default_controller

config = get_config()


class Home(Base):
    __table__ = Table(
        'homes',
        Base.metadata,
        autoload_with=get_default_controller().get_engine()
    )
