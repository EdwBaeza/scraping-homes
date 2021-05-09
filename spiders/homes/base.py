from abc import ABC, abstractmethod

from spiders.base import Base


class BaseHomeSpider(Base, ABC):

    def __init__(self, browser_builder):
        super(Base, self).__init__(browser_builder)

    @abstractmethod
    def extract_title(self):
        pass

    @abstractmethod
    def extract_description(self):
        pass

    @abstractmethod
    def extract_location(self):
        pass

    @abstractmethod
    def extract_address(self):
        pass

    @abstractmethod
    def extract_price(self):
        pass

    @abstractmethod
    def extract_common_features(self):
        pass

    @abstractmethod
    def extract_extra_features(self):
        pass

    @abstractmethod
    def paginate(self):
        pass

    @abstractmethod
    def get_links(self):
        pass

    @abstractmethod
    def get_data(self):
        pass
