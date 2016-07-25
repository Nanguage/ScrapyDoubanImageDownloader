# -*- coding: utf-8 -*-

import scrapy


class DoubanPicItem(scrapy.Item):
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    images = scrapy.Field()
    subject_id = scrapy.Field()
