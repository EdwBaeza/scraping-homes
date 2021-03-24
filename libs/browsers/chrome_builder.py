from selenium import webdriver

from libs.browsers.base_builder import BaseBuilder


class ChromeBuilder(BaseBuilder):

    def __init__(self):
        self._options = webdriver.ChromeOptions()
        self._browser = None

    @property
    def browser(self):
        self._browser = webdriver.Chrome(chrome_options=self._options)

        return self._browser

    def add_general_settings(self):
        self._options.add_argument(f"window-size=1920,1080")
        self._options.add_argument('--no-sandbox')
        self._options.add_argument('--disable-gpu')
        self._options.add_argument('--hide-scrollbars')
        self._options.add_argument('--disable-popup-blocking')
        self._options.add_argument('--disable-infobars')
        self._options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36")
        self._options.add_argument('--ignore-certificate-errors')
        self._options.add_experimental_option('prefs', { 'intl.accept_languages': 'es-MX' })

    def add_docker_settings(self):
        self._options.add_argument('--disable-dev-shm-usage')
        self._options.add_argument('--single-process')
        self._options.add_argument('--user-data-dir=/tmp/user-data')
        self._options.add_argument('--data-path=/tmp/data-path')
        self._options.add_argument('--homedir=/tmp')
        self._options.add_argument('--disk-cache-dir=/tmp/cache-dir')

    def add_headless_settings(self):
        self._options.add_argument('--headless')
