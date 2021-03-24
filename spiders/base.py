from abc import ABC
import random
import time
import uuid

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class Base(ABC):

    def __init__(self, browser_builder, **kwargs):
        self._headless = kwargs.get('headless', False)
        self._builder = browser_builder
        self.browser = self._get_browser()

    def _get_browser(self):
        self._builder.add_general_settings()
        self._builder.add_docker_settings()

        if self._headless:
            self._builder.add_headless_settings()

        return self._builder.browser

    def time_sleep(self, time_to_sleep=3.0):
        time.sleep(time_to_sleep)

    def random_time_sleep(self):
        self.time_sleep(random.randint(1, 5))

    def kill_browser(self):
        self.browser.quit()

    def navigate(self, url):
        self.browser.get(url)

    def get_content(self):
        return self.browser.page_source.encode('utf8')

    def get_content_soup(self):
        return BeautifulSoup(self.get_content(), 'html.parser')

    def get_html_tag(self):
        return self.browser.find_element_by_tag_name('html')

    def page_down(self):
        html = self.get_html_tag()
        html.send_keys(Keys.PAGE_DOWN)
        html.send_keys(Keys.PAGE_DOWN)

    def page_up(self):
        html = self.get_html_tag()
        html.send_keys(Keys.PAGE_UP)
        html.send_keys(Keys.PAGE_UP)

    def scroll_to_end(self):
        html = self.get_html_tag()
        for index in range(10):
            html.send_keys(Keys.PAGE_DOWN)
            self.time_sleep(1.0)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def screenshot(self):
        uuid4 = str(uuid.uuid4())
        full_name = f"./screenshot_{uuid4}.png"
        self.browser.save_screenshot(full_name)

    def move_to_element(self, element):
        action_chains = ActionChains(self.browser)
        action_chains.move_to_element(element).perform()
        self.time_sleep(1.5)
        self.browser.execute_script("window.scrollBy(0, -150);")
