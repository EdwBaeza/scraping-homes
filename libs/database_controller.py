
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from libs.config import get_config


class DatabaseController(object):
    """ DatabaseController """
    drive = 'postgresql+psycopg2'

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
        self.engine = self.get_engine()

    def get_engine(self):
        """ create and return engine"""
        access = f"{self.user}:{self.password}@{self.host}/{self.name}"
        return create_engine(f"{self.drive}://{access}")

    def get_session(self):
        """ start connection to database"""
        try:
            DBSession = sessionmaker(bind=self.engine, autoflush=True)
            session = DBSession()
        except Exception as e:
            raise e
        else:
            return session

    def get_table(self, table_name):
        """ return table using reflected"""
        return Table(table_name, MetaData(), autoload_with=self.engine)


def get_default_controller():
    config = get_config()

    return DatabaseController(
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            host=config.POSTGRES_HOST,
            name=config.POSTGRES_DB
        )
