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
        # ':authority':'',
        # ':method':'GET',
        # ':scheme':'https',
        # ':path':'',
        # 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'accept-encoding':'gzip, deflate, sdch, br',
        # 'accept-language':'zh-CN,zh;q=0.8',
        # 'cache-control':'max-age=0',
        # 'cookie':'bid=asp_vcGM4-s',
        # 'if-modified-since':'Wed, 21 Jan 2004 19:51:30 GMT',
        # 'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'referer': '',
    }


    def get_media_requests(self, item, info):
        return [Request(x, headers=self.get_headers(x), meta={'subject_id':item['subject_id']}) \
                for x in item.get(self.images_urls_field, [])]

    # def get_media_requests(self, item, info):
        # for image_url in item['image_urls']:
            # headers = self.get_headers(image_url)
            # # yield scrapy.Request(image_url)
            # yield scrapy.Request(image_url, meta={'cookiejar':1}, headers=headers)
            # # yield scrapy.Request(image_url, headers=headers)

    CONVERTED_ORIGINAL = re.compile('^full/[0-9,a-f]+.jpg$')

    def get_images(self, response, request, info):
        print("get images")
        for key, image, buf, in super(DoubanPicPipeline, self).get_images(response, request, info):
            if self.CONVERTED_ORIGINAL.match(key):
                key = self.change_filename(key, response)
            yield key, image, buf

    def change_filename(self, key, response):
        return key.replace('full', response.meta['subject_id'])

    # def item_completed(self, results, item, info):
        # image_paths = [x['path'] for ok, x in results if ok]
        # if not image_paths:
            # raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        # return item

    def get_headers(self, url):
        headers = self.headers
        #change headers
        aut = url.split('/')[2]
        path = url[25:]
        ref = re.sub(r'img\d\.doubanio\.com/view/photo/raw/public/p(.*)\.jpg', \
                r'movie.douban.com/photos/photo/\g<1>/', url)
        # headers[':authority'] = aut
        # headers[':path'] = path
        headers['referer'] = ref
        return headers

