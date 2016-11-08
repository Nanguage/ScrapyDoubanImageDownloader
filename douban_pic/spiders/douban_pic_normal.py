# -*- coding: utf-8 -*-

import re
import os
import shutil
import logging
import subprocess

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.selector import Selector

from douban_pic.items import DoubanPicItem
from douban_pic.settings import IMAGES_STORE
from douban_pic.settings import ALBUMS


ALBUMS = {url: name for name, url in ALBUMS.items()}
id2name = {re.match('.*/(\d+)/.*$', url).group(1): name for url, name in ALBUMS.items()}


class PicCrawlSpider(CrawlSpider):
    name = "douban_pic"
    # download_delay = 0.1

    allowed_domains = []

    start_urls = ALBUMS.keys()

    rules = (
            Rule(LinkExtractor(allow=(r'https://movie\.douban\.com/subject/\d+/.+')),
                callback='parse_item', follow=True),        
    )
        
    # mkdir for store image
    for url in start_urls:
        subject_name = ALBUMS[url]
        path = os.path.join(IMAGES_STORE, subject_name)
        if os.path.exists(path): 
            yes = raw_input("{path} already exist remove it? [n]/y ?".format(path=path))
            if yes == 'y' or 'yes':
                shutil.rmtree(path)
            else:
                raise OSError('{path} already exist! '.format(path=path))
        os.mkdir(path)

    def parse_item(self, response):
        subject_id = re.match('.*/(\d+)/.*$', response.url).group(1)
        subject_name = id2name[subject_id]
        sel = Selector(response)
        img_paths = sel.xpath('//li[@data-id]/div/a/img[@src]/@src').extract()

        for path in img_paths:
            item = DoubanPicItem()

            img_path = path.replace('thumb', 'raw')
            # img_path = path.replace('thumb', 'photo')
            print "="*30
            logging.log(logging.DEBUG, img_path)

            item['image_urls'] = [img_path]
            item['subject_id'] = subject_id
            item['subject_name'] = subject_name
            yield item
