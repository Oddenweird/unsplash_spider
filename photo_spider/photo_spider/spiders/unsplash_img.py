import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.loader import ItemLoader
from ..items import PhotoSpiderItem
from itemloaders.processors import MapCompose
from urllib.parse import urljoin

class UnsplashImgSpider(CrawlSpider):
    name = "unsplash_img"
    allowed_domains = ["unsplash.com", "images.unsplash.com", "plus.unsplash.com"]
    start_urls = ["https://unsplash.com"]

    rules = (Rule(LinkExtractor(restrict_xpaths=('//a[@class="zNNw1"]')), callback="parse_item", follow=True),    
             Rule(LinkExtractor(restrict_xpaths=('//div[@class="qaAX1"]//a[@class="wuIW2 R6ToQ"]')))
            )

    def parse_item(self, response):
        # print(response.url)
        loader = ItemLoader(item=PhotoSpiderItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        
        loader.add_xpath('name', '//h1[@class="vev3s"]/text()')

        relative_category_images = response.xpath('//a[@class="vGXaw uoMSP kXLw7 R6ToQ JVs7s R6ToQ"]/text()').getall()
        loader.add_value('category_images',relative_category_images)
       
        # relative_images_urls = response.xpath('//div[@class="wdUrX"]/img[@class="I7OuT DVW3V L1BOa"]/@src').get()
        # loader.add_value('images_urls', relative_images_urls)

        # relative_images_urls = response.xpath('//div[@class="wdUrX"]/img[@class="I7OuT DVW3V L1BOa"]/@src').get()
        # absolute_images_urls = [urljoin(response.url, img_url) for img_url in relative_images_urls]
        # loader.add_value('images_urls', absolute_images_urls)

        relative_images_urls = response.xpath('//div[@class="wdUrX"]/img[@class="I7OuT DVW3V L1BOa"]/@src').get()
        # if not relative_images_urls:
        #     self.logger.warning("No image URLs found on the page: %s", response.url)
        absolute_images_urls = [urljoin(response.url, url) for url in relative_images_urls]
        if not absolute_images_urls:
            self.logger.warning("No image URLs found on the page: %s", response.url)

        loader.add_value('images_urls', absolute_images_urls)
                         
        
        yield loader.load_item()
# //a[@class="m7tXD jhw7y TYpvC"]/text() - теги фотографий
# //div[@class="qaAX1"]//a[@class="wuIW2 R6ToQ"] - вместо кнопки некст
# //a[@class="wuIW2 R6ToQ"] - для перехода по категориям.
# //div[@class="wdUrX"]/div[@class="SpgDA"] - для перехода по фотографиям
# //div[@class="JM3zT"]/a - для извлечения url фотографии
# //h1[@class="vev3s"]/text() - для названия фотографии
# //a[@class="wuIW2 R6ToQ"]//ya-tr-span/text() - для текста категорий