import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import NoSuchElementException

from ..items import ScrapyMangoItem


class MangoSpider(scrapy.Spider):
    name = 'mangospider'
    # start_urls = ['https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99']

    def start_requests(self):
        url = 'https://shop.mango.com/gb/women/skirts-midi/midi-satin-skirt_17042020.html?c=99'
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        item: ScrapyMangoItem = ScrapyMangoItem()
        item['name'] = response.xpath("//h1[@class='product-name']/text()").get().strip()
        item['color'] = response.xpath("//div[@id='colorsContainer']/div[contains(@aria-label, 'selected')]/@aria-label")\
            .get().replace(" selected","").strip()
        item['price'] = response.xpath("//span[@data-testid='currentPrice']//text()").get().strip()
        item['size'] = self.__get_sizes(response)


        return {
            item
        }

    def __get_sizes(self, response):
        list_of_sizes = []

        size_base_locator = "//ul[@aria-label='Select your size']/li"
        sizes = response.xpath(size_base_locator + "//span[1]/text()").getall()

        for i, el in enumerate(sizes):
            try:
                response.xpath(size_base_locator + f"[{i + 1}]/button[not(contains(@data-testid, 'unavailable'))]")
                is_available = "available"
            except NoSuchElementException:
                is_available = "unavailable"

            list_of_sizes.append({el: is_available})

        return list_of_sizes