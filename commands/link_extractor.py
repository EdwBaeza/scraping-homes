import logging
from datetime import datetime, timezone

from sqlalchemy import select, insert

from models.home import Home
from commands.base import Base

from libs.database_controller import get_default_controller


class LinkExtractor(Base):

    def __init__(self, spider, **kwargs):
        self.logger = logging.getLogger()
        self.controller = get_default_controller()
        self.session = self.controller.get_session()
        self.spider = spider

    def execute(self):
        self.logger.info("Extracting links...")
        links = self.spider.get_links()
        self.logger.info("Links extracted: %d", len(links))

        for link in links:
            self.logger.info("Current url %s", link)
            if self._exist_url(link):
                self.logger.info("Url already exists")
                continue

            self._insert_link_extracted(link)

    def _insert_link_extracted(self, url):
        self.session.add(
            Home(
                url=url,
                site=self.spider.NAME,
                created_at=datetime.now(timezone.utc)
            )
        )
        self.session.commit()
        self.session.close()

    def _exist_url(self, url):
        query = select(Home).where(Home.url == url)
        return self.session.execute(query).fetchone()

