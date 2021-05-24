import logging
from datetime import datetime, timezone

from models.home import Home
from commands.base import Base

from libs.database_controller import get_default_controller

from libs.config import get_config

class HomeExtractor(Base):

    def __init__(self, spider, **kwargs):
        self.__config = get_config()
        self.logger = logging.getLogger()
        self.controller = get_default_controller()
        self.session = self.controller.get_session()
        self.spider = spider

    def execute(self):
        self.logger.info("Extracting Homes...")
        homes = self.__get_homes()
        self.logger.info("Homes to extracted: %d", len(homes))

        for home in homes:
            self.logger.info("Current Home: %s", home.url)
            update_stmp = Home.__table__.update(Home.id == home.id).values(**self.spider.get_data(home.url))
            self.session.execute(update_stmp)
            self.session.commit()

    def __get_homes(self):
        return self.session\
                    .query(Home)\
                    .filter(Home.extracted_at.is_(None) & Home.url.isnot(None))\
                    .limit(self.__max_items())\
                    .all()

    def __max_items(self):
        self.__config.tasks.get("home_extractor", {}).get("max_items", 200)
