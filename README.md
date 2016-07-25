# 豆瓣相册图片下载器
使用scrapy框架编写
## 使用方法
安装scrapy:
```
pip install scrapy
```

修改./douban_pic/settings.py:
```
# 图片的存放地址
IMAGES_STORE = '/store/path/'
```

修改./douban_pic/spiders/pic_crawl.py:
```
    start_urls = (
        # 逐个填入待爬取相册的url,例如：
        'https://movie.douban.com/subject/26411388/photos?type=S', 
        'https://movie.douban.com/subject/1300798/photos?type=S',
    )
```


运行:
```
$ scrapy crawl douban_pic
```
