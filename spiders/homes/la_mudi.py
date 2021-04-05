from spiders.homes.base import BaseHomeSpider


class LaMudi(BaseHomeSpider):
    name = "la_mudi"
    URL = "https://www.lamudi.com.mx/yucatan/merida/casa/for-sale/"
    NEXT_PAGE_BUTTON_CSS = ".next > a"
    HOME_LINK_ELEMENT_CSS = ".ListingCell-TitleWrapper > h2 > a"
    TITLE_CSS = ".Header-title-block > h1"
    DESCRIPTION_CSS = ".ViewMore-text div.ViewMore-text-description"

    def __init__(self, browser_builder, **kwargs):
        super(BaseHomeSpider, self).__init__(browser_builder, **kwargs)

    def extract_title(self):
        return self.get_string_by_css(self.TITLE_CSS)

    def extract_description(self):
        pass

    def extract_location(self):
        pass

    def extract_address(self):
        pass

    def extract_price(self):
        pass

    def extract_common_features(self):
        pass

    def paginate(self):
        try:
            self.scroll_to_end()
            next_page_button = self.browser.find_element_by_css_selector(self.NEXT_PAGE_BUTTON_CSS)
            self.move_to_element(next_page_button)
            next_page_button.click()
            self.random_time_sleep()
        except Exception as e:
            self.logger.error(e)
            self.screenshot()
            return False
        else:
            return True

    def get_links(self):
        elements = []

        self.navigate(self.URL)
        while True:
            elements += self.get_elements_by_css(self.HOME_LINK_ELEMENT_CSS)
            self.logger.info("Urls extracted now: %d", len(elements))

            if not self.paginate():
                break

        return [element['href'] for element in elements]

    def get_data(self, url):
        self.navigate(url)

        return {
            'url': url,
            'title': self.extract_title()
        }
