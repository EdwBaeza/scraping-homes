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
        location_element = self.get_element_by_css("#js-developmentMap") or {}

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

        return {
            "rooms": self.get_numeric_by_css("span.Overview-attribute.icon-bedrooms-v4"),
            'baths': self.get_numeric_by_css('.ellipsis[data-attr-name="bathrooms"] + div'),
            'parking_lots': self.get_numeric_by_css('.ellipsis[data-attr-name="car_spaces"] + div'),
            "square_meter": clean_meters(self.get_string_by_css("span.Overview-attribute.icon-land_size-v4")),
            "building_square_meter": clean_meters(self.get_string_by_css("span.icon-livingsize-v4.Overview-attribute"))
        }

    def extract_extra_features(self):
        return {
            "agent_name": self.get_string_by_css("div.AgentInfoV2-agent-name"),
            "full_address": self.get_string_by_css("span.Header-title-address-text"),
            "la_mudi":  self.la_mudi_insights()

        }

    def la_mudi_insights(self):
        insights = {
            "neighborhood_score": self.get_string_by_css("div.AreaRating-Overall")
        }
        elements = self.get_elements_by_css(".AreaRatingStars-container div.Rating-container")

        for element in elements:
            if len(element) > 1:
                first, second = [*element]
                stars = len(second.select(".icon-star"))
                stars +=  0.5 if second.select_one(".icon-star-half") else 0.0
                insights[first.get_text().strip()] = stars

        return insights

    def extract_date_out(self):
        data = self.get_string_by_css('div[data-attr-name="empty"] + div')

        return datetime.strptime(data.strip(), "%d/%m/%y") if data else None

    def extract_building_year(self):
        return self.get_numeric_by_css('div[data-attr-name="year_built"] + div')

    def extract_total_rooms(self):
        return self.get_numeric_by_css('div[data-attr-name="rooms_total"] + div')

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
            elements += self.get_elements_by_css(self, home_link_element_css)
            self.logger.info("Urls extracted now: %d", len(elements))

            if not self.paginate():
                self.logger.info("finished page: %s", self.browser.current_url)
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
            "extracted_at": datetime.now(timezone.utc),
            "date_out": self.extract_date_out(),
            "building_year": self.extract_building_year(),
            "total_rooms": self.extract_total_rooms()
        }
