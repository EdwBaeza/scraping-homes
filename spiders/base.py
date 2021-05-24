import random
import time
import uuid
import logging
from abc import ABC

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class Base(ABC):

    def __init__(self, browser_builder):
        self.__builder = browser_builder
        self.browser = self.__get_browser()
        self.logger = logging.getLogger()

    def __get_browser(self):
        self.__builder.add_general_settings()
        self.__builder.add_docker_settings()
        self.__builder.add_headless_settings()

        return self.__builder.browser

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

    def get_string_by_css(self, css):
        element = self.get_element_by_css(css)
        return element.get_text() if element else None

    def get_element_by_css(self, css):
        page = self.get_content_soup()
        return page.select_one(css)

    def get_elements_by_css(self, css):
        page = self.get_content_soup()
        return page.select(css)

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
        full_name = f"./screenshot_{self.NAME}_{uuid4}.png"
        self.browser.save_screenshot(full_name)

    def move_to_element(self, element):
        action_chains = ActionChains(self.browser)
        action_chains.move_to_element(element).perform()
        self.time_sleep(1.5)
        self.browser.execute_script("window.scrollBy(0, -150);")
