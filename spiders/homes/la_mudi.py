from spiders.homes.base import BaseHomeSpider


class LaMudi(BaseHomeSpider):

    URL = 'https://www.lamudi.com.mx/yucatan/merida/casa/for-sale/'

    def __init__(self, browser_builder, **kwargs):
        super(BaseHomeSpider, self).__init__(browser_builder, **kwargs)

    def extract_title(self):
        CSS = '.Header-title-block > h1'
        page = self.get_content_soup()
        title_element = page.select_one(CSS)

        return title_element.get_text() if title_element else None

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
            NEXT_PAGE_BUTTON_CSS = '.next > a'
            self.scroll_to_end()
            next_page_button = self.browser.find_element_by_css_selector(NEXT_PAGE_BUTTON_CSS)
            self.move_to_element(next_page_button)
            next_page_button.click()
            self.random_time_sleep()
        except Exception as e:
            print(e)
            self.screenshot()
            return False
        else:
            return True

    def get_links(self):
        A_ELEMENT_CSS = '.ListingCell-TitleWrapper > h2 > a'
        elements = []

        self.navigate(self.URL)
        while True:
            soup = self.get_content_soup()
            elements+= soup.select(A_ELEMENT_CSS)

            if not self.paginate():
                break

        return [element['url'] for element in elements]

    def get_data(self, url):
        self.navigate(url)

        return {
            'url': url,
            'title': self.extract_title()
        }
