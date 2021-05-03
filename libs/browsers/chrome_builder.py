import random
from selenium import webdriver

from libs.config import get_config
from libs.browsers.base_builder import BaseBuilder


class ChromeBuilder(BaseBuilder):

    def __init__(self):
        self._options = webdriver.ChromeOptions()
        self._config = get_config()
        self._browser = None

    @property
    def browser(self):
        self._browser = webdriver.Chrome(chrome_options=self._options)

        return self._browser

    def add_general_settings(self):
        size = self._get_item("sizes")
        user_agent = self._get_item("user_agents")
        language = self._config.browser["languages"]
        self._options.add_argument(f"window-size={size}")
        self._options.add_argument("--no-sandbox")
        self._options.add_argument("--disable-gpu")
        self._options.add_argument("--hide-scrollbars")
        self._options.add_argument("--disable-popup-blocking")
        self._options.add_argument("--disable-infobars")
        self._options.add_argument(f"user-agent={user_agent}")
        self._options.add_argument("--ignore-certificate-errors")
        self._options.add_experimental_option("prefs", { "intl.accept_languages": language })

    def add_docker_settings(self):
        self._options.add_argument('--disable-dev-shm-usage')
        self._options.add_argument('--single-process')
        self._options.add_argument('--user-data-dir=/tmp/user-data')
        self._options.add_argument('--data-path=/tmp/data-path')
        self._options.add_argument('--homedir=/tmp')
        self._options.add_argument('--disk-cache-dir=/tmp/cache-dir')

    def add_headless_settings(self):
        if self._config.browser["headless"]:
            self._options.add_argument('--headless')

    def _get_item(self, key):
        data = self._config.browser[key]
        size = len(data) - 1
        assert size > 0, f'Data not found {key}'
        return data[random.randint(0, size)]
