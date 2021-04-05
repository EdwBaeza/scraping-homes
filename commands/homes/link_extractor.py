import logging
from datetime import datetime, timezone

from sqlalchemy import select, insert

from models.home import Home
from commands.base import Base
from spiders.homes.la_mudi import LaMudi

from libs.config import get_config
from libs.browsers.chrome_builder import ChromeBuilder
from libs.database_controller import get_default_controller


class LinkExtractor(Base):

    def __init__(self, spider, **kwargs):
        self.config = get_config()
        self.logger = logging.getLogger()
        self.controller = get_default_controller()
        self.session = self.controller.get_session()
        self.spider = spider

    def execute(self):
        self.logger.info("Extracting links...")
        links = self.spider.get_links()

        self.logger.info("Links extracted: %d", len(links))
        for link in links:
            self._insert_link_extracted(link)

    def _insert_link_extracted(self, url):
        query = select(Home).where(Home.url == url)

        if self.session.execute(query).fetchone():
            self.logger.info("Url already exists")
            return

        self.logger.info("Inserting url %s", url)
        utc_current_datetime = datetime.now(timezone.utc)
        self.session.add(
            Home(
                url=url,
                site=self.spider.name,
                created_at=utc_current_datetime
            )
        )
        self.session.commit()
        self.session.close()
