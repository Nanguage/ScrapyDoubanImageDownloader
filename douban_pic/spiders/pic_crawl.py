# -*- coding: utf-8 -*-

import re
import os
import shutil
import logging
import subprocess

# from scrapy.utils.response import open_in_browser
# from scrapy.shell import inspect_response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from douban_pic.items import DoubanPicItem
from douban_pic.settings import IMAGES_STORE

class PicCrawlSpider(CrawlSpider):
    name = "douban_pic"
    download_delay = 0.1

    allowed_domains = []

    start_urls = (
        # 填入待爬取相册的url
        'https://movie.douban.com/subject/26411388/photos?type=S', 
    )

    rules = (
            Rule(LinkExtractor(allow=(r'https://movie\.douban\.com/subject/\d+/.+')),
                callback='parse_item', follow=True),        
    )
        
    # mkdir for store image
    for url in start_urls:
        subject_id = re.match('.*/(\d+)/.*$', url).group(1)
        path = IMAGES_STORE + str(subject_id)
        if os.path.exists(path): shutil.rmtree(path)
        os.mkdir(path)

    def parse_item(self, response):
        # inspect_response(response,self)
        subject_id = re.match('.*/(\d+)/.*$', response.url).group(1)
        sel = Selector(response)
        img_paths = sel.xpath('//li[@data-id]/div/a/img[@src]/@src').extract()

        for path in img_paths:
            item = DoubanPicItem()

            img_path = path.replace('thumb', 'raw')
            print "="*30
            logging.log(logging.DEBUG, img_path)

            item['image_urls'] = [img_path]
            item['subject_id'] = subject_id
            yield item
