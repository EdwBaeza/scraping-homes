from commands.base import Base
from spiders.homes.la_mudi import LaMudi
from libs.config import get_config
from libs.browsers.chrome_builder import ChromeBuilder
from libs.database_controller import get_default_controller


class LaMudiLinkExtractor(Base):

    def __init__(self, **kwargs):
        self.config = get_config()
        self.controller = get_default_controller()
        self.spider = LaMudi(ChromeBuilder(), **self.config.browser)

    def execute(self):
        self.spider.get_links()

    def _insert_link_extracted(self):
        pass
