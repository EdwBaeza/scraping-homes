from datetime import datetime, timezone

from spiders.homes.base import BaseHomeSpider


class LaMudi(BaseHomeSpider):
    NAME = "la_mudi"
    URL = "https://www.lamudi.com.mx/yucatan/merida/casa/for-sale/"

    def __init__(self, browser_builder):
        super(BaseHomeSpider, self).__init__(browser_builder)

    def extract_title(self):
        return self.get_string_by_css(".Header-title-block > h1")

    def extract_description(self):
        return self.get_string_by_css(".ViewMore-text div.ViewMore-text-description")

    def extract_location(self):
        location_element = self.get_content_soup().select_one("#js-developmentMap") or {}

        return {
            "latitude": location_element.get("data-lat"),
            "longitude": location_element.get("data-lng")
        }

    def extract_address(self):
        pass

    def extract_price(self):
        price = self.get_string_by_css("span.FirstPrice")
        return float(price.replace(',', '').replace('$', '').strip()) if price else None

    def extract_common_features(self):
        clean_meters = lambda square_meter: float(square_meter.replace("m²", "").strip()) if square_meter else None
        rooms = self.get_string_by_css("span.Overview-attribute.icon-bedrooms-v4")
        baths = self.get_string_by_css('.ellipsis[data-attr-name="bathrooms"] + div')
        parking_lots = self.get_string_by_css('.ellipsis[data-attr-name="car_spaces"] + div')
        square_meter = self.get_string_by_css("span.Overview-attribute.icon-land_size-v4")
        building_square_meter = self.get_string_by_css("span.icon-livingsize-v4.Overview-attribute")

        return {
            "rooms": float(rooms.strip()) if rooms else None,
            'baths': float(baths.strip()) if baths else None,
            'parking_lots': float(parking_lots.strip()) if parking_lots else None,
            "square_meter": clean_meters(square_meter),
            "building_square_meter": clean_meters(building_square_meter)
        }

    def extract_extra_features(self):
        agent_name = self.get_string_by_css("div.AgentInfoV2-agent-name")
        full_address = self.get_string_by_css("span.Header-title-address-text")

        return {
            'agent_name': agent_name.strip() if agent_name else None,
            'full_address': full_address.strip() if full_address else None
        }

    def paginate(self):
        try:
            self.scroll_to_end()
            next_page_button = self.browser.find_element_by_css_selector(".next > a")
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
        home_link_element_css = ".ListingCell-TitleWrapper > h2 > a"
        elements = []

        self.navigate(self.URL)
        while True:
            elements += self.get_content_soup().select(home_link_element_css)
            self.logger.info("Urls extracted now: %d", len(elements))

            if not self.paginate():
                break

        return [element['href'] for element in elements]

    def get_data(self, url):
        self.navigate(url)
        price = self.extract_price()
        common_features = self.extract_common_features()
        square_meter = common_features.get("square_meter")
        return {
            "url": url,
            "title": self.extract_title(),
            "description": self.extract_description(),
            "price": price,
            "price_per_square_meter": price / square_meter if square_meter and price else None,
            'extra_features': self.extract_extra_features(),
            **common_features,
            **self.extract_location(),
            'extracted_at': datetime.now(timezone.utc)
        }
