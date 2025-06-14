import json
import re

import scrapy
from auto_ria.items import CarItem
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class AutoRiaSpider(scrapy.Spider):
    name = 'autoria'
    allowed_domains = ['auto.ria.com']
    start_urls = [os.getenv('START_URL')]

    def parse(self, response):
        car_links = response.css('a.address::attr(href)').getall()
        used_car_links = [
            link for link in car_links
            if '/auto_' in link and '/newauto/' not in link and '/truck_' not in link
        ]
        self.logger.info(f"next car count = {len(used_car_links)}")

        for link in used_car_links:
            self.logger.info(f"Start parsing: {link}")
            yield response.follow(link, callback=self.parse_car)

        next_page = response.css('a.page-link.js-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_car(self, response):
        item = CarItem()
        item['url'] = response.url
        item['title'] = response.css('h1.head::text').get(default='').strip()
        price_text = response.css('div.price_value strong::text').get()
        if price_text:
            price = price_text.replace('$', '').replace(' ', '').replace('\xa0', '')
            try:
                item['price_usd'] = int(price)
            except ValueError:
                item['price_usd'] = None
        else:
            item['price_usd'] = None

        odometer_str = response.css('div.base-information span::text').get()
        if odometer_str:
            odometer_str += "000"
            item['odometer'] = int(odometer_str)
        else:
            item['odometer'] = None

        user_name = response.css('.seller_info_name::text').get(default='').strip() or response.css('.seller_info_name a::text').get(default='').strip()
        item['username'] = user_name

        item['phone_number'] = None

        item['image_url'] = response.css('.photo-620x465 img::attr(src)').get()

        images_count_str = response.css('div.count-photo span.mhide::text').get()
        item['images_count'] = int(images_count_str.split(" ")[1]) if images_count_str else None

        car_number = response.xpath("//span[contains(@class, 'state-num')]/text()").get()
        item['car_number'] = car_number.strip() if car_number else None

        vin_code = self.extract_text(response, 'VIN-код')
        item['car_vin'] = vin_code if vin_code else None

        item['datetime_found'] = datetime.utcnow()

        advertisement_id_match = re.search(r'_(\d+)\.html$', response.url)
        if not advertisement_id_match:
            self.logger.warning(f'advertisement_id is not found in URL: {response.url}')
            yield item
            return

        advertisement_id = advertisement_id_match.group(1)

        user_id = response.css(f"script[data-advertisement-id='{advertisement_id}']").attrib.get("data-owner-id")

        if not user_id:
            self.logger.warning(f'data-owner-id is not found for URL: {response.url}')
            yield item
            return

        phone_hash = response.css(f'script.js-user-secure-{user_id}::attr(data-hash)').get()
        expires = response.css(f'script.js-user-secure-{user_id}::attr(data-expires)').get()

        if phone_hash and expires:
            phone_url = f'https://auto.ria.com/users/phones/{advertisement_id}?hash={phone_hash}&expires={expires}'
            yield scrapy.Request(
                url=phone_url,
                callback=self.parse_phone,
                meta={'item': item},
                headers={
                    'Referer': response.url,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            )
        else:
            yield item

    def extract_text(self, response, label):
        xpath_expr = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{label.lower()}')]/following-sibling::span[1]/text()"
        node = response.xpath(xpath_expr).get()
        return node.strip() if node else None

    def parse_phone(self, response):
        item = response.meta['item']
        try:
            data = json.loads(response.text)
            item['phone_number'] = self.normalize_phone(data.get('formattedPhoneNumber'))
        except Exception as e:
            self.logger.warning(f"Cannot parse phone_number: {e}")

        yield item

    @staticmethod
    def normalize_phone(phone):
        digits = re.sub(r'\D', '', phone)

        if len(digits) == 10 and digits.startswith('0'):
            return '+38' + digits

        if len(digits) == 12 and digits.startswith('380'):
            return '+' + digits

        return None


