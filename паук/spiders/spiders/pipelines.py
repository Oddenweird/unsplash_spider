# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import hashlib

class SpidersImagePipeline:
    def process_item(self, item, spider):
        return item
    
# import scrapy
# from scrapy.pipelines.images import ImagesPipeline
# from scrapy.exceptions import DropItem
# from itemadapter import ItemAdapter

# class SpidersImagePipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         # Извлекаем URL изображений и создаем запросы для их скачивания
#         for image_url in item.get('images_urls', []):
#             yield scrapy.Request(image_url)

#     def file_path(self, request, response=None, info=None):
#         # Сохраняем файл с оригинальным именем
#         # return request.url.split('/')[-1]  # Получаем имя файла из URL
#         return super().file_path(request, response, info)

#     def item_completed(self, results, item, info):
#         # Проверяем, были ли загружены изображения
#         if not any(result[0] for result in results):
#             raise DropItem("Image not downloaded")
#         return item