# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PhotoSpiderItem(scrapy.Item):
    category_images = scrapy.Field()
    name = scrapy.Field()
    images_urls = scrapy.Field()
    images = scrapy.Field()