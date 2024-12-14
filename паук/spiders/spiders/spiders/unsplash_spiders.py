import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import SpidersItem
from itemloaders.processors import MapCompose
from urllib.parse import urljoin


class UnsplashSpidersSpider(CrawlSpider):
    name = "unsplash_spiders"
    allowed_domains = ["unsplash.com", "plus.unsplash.com", "images.unsplash.com"]
    start_urls = ["https://unsplash.com"]

    rules = (Rule(LinkExtractor(restrict_xpaths=('//a[@class="mG0SP"]')), callback="parse_item", follow=True),
            Rule(LinkExtractor(restrict_xpaths=('//div[@class="UNOZg"]//a[@class="Y8n01 KZwZl"]'))) #для перехода по сайту.
            )
    # //div[@class="NrLlp"]/div[@class="xH5KD"]/img[@class="tzC2N fbGdz cnmNG"]/@src
    def parse_item(self, response):
        print(response.url)
        loader = ItemLoader(item=SpidersItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        
        loader.add_xpath('name', '//h1[@class="SJYb8"]/text()')   
        loader.add_xpath('tags_images','//a[@class="qOAId yZhvJ FTKrh"]/text()')    
        loader.add_xpath('images_urls','//div[@class="NrLlp"]/div[@class="xH5KD"]/img[@class="tzC2N fbGdz cnmNG"]/@src') #Здесь не установлена getall из-за того, что она не нужна здесь. Для программы необходимо вытащить только одну фотографию
        # Все остальные ссылки на фотографии в коде различаются только маштабированием, что на мой взгляд не интересуется в задании.

        # loader.add_xpath('images','//img[@style="display: block;-webkit-user-select: none;margin: auto;cursor: zoom-in;background-color: hsl(0, 0%, 90%);transition: background-color 300ms;"]/@src')
# //a[@class="qOAId yZhvJ FTKrh"]/text()
        yield loader.load_item()
