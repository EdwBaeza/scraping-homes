import random
from selenium import webdriver

from libs.config import get_config
from libs.browsers.base_builder import BaseBuilder


class ChromeBuilder(BaseBuilder):

    def __init__(self):
        self.__options = webdriver.ChromeOptions()
        self.__config = get_config()
        self.__browser = None

    @property
    def browser(self):
        self.__browser = webdriver.Chrome(chrome_options=self.__options)

        return self.__browser

    def add_general_settings(self):
        size = self.__get_item("sizes")
        user_agent = self.__get_item("user_agents")
        language = self.__config.browser["languages"]
        self.__options.add_argument(f"window-size={size}")
        self.__options.add_argument("--no-sandbox")
        self.__options.add_argument("--disable-gpu")
        self.__options.add_argument("--hide-scrollbars")
        self.__options.add_argument("--disable-popup-blocking")
        self.__options.add_argument("--disable-infobars")
        self.__options.add_argument(f"user-agent={user_agent}")
        self.__options.add_argument("--ignore-certificate-errors")
        self.__options.add_experimental_option("prefs", { "intl.accept_languages": language })

    def add_docker_settings(self):
        self.__options.add_argument('--disable-dev-shm-usage')
        self.__options.add_argument('--single-process')
        self.__options.add_argument('--user-data-dir=/tmp/user-data')
        self.__options.add_argument('--data-path=/tmp/data-path')
        self.__options.add_argument('--homedir=/tmp')
        self.__options.add_argument('--disk-cache-dir=/tmp/cache-dir')

    def add_headless_settings(self):
        if self.__config.browser["headless"]:
            self.__options.add_argument('--headless')

    def __get_item(self, key):
        data = self.__config.browser[key]
        size = len(data) - 1
        assert size > 0, f'Data not found {key}'
        return data[random.randint(0, size)]
