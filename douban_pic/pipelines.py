# -*- coding: utf-8 -*-

import re

import scrapy
from scrapy.http import Request
# from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanPicPipeline(ImagesPipeline):
    
    headers = {
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'referer': '',
    }


    def get_media_requests(self, item, info):
        return [Request(x, headers=self.get_headers(x), meta={'subject_id':item['subject_id'], \
                'subject_name':item['subject_name']}) for x in item.get(self.images_urls_field, [])]

    CONVERTED_ORIGINAL = re.compile('^full/[0-9,a-f]+.jpg$')

    def get_images(self, response, request, info):
        print("get images")
        for key, image, buf, in super(DoubanPicPipeline, self).get_images(response, request, info):
            if self.CONVERTED_ORIGINAL.match(key):
                key = self.change_filename(key, response)
            yield key, image, buf

    def change_filename(self, key, response):
        return key.replace('full', response.meta['subject_name'])

    def get_headers(self, url):
        headers = self.headers
        #change headers
        aut = url.split('/')[2]
        path = url[25:]
        ref = re.sub(r'img\d\.doubanio\.com/view/photo/raw/public/p(.*)\.jpg', \
                r'movie.douban.com/photos/photo/\g<1>/', url)
        headers['referer'] = ref
        return headers

