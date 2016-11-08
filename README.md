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

# 逐个填入待爬取相册的 name: url 键值对 如下:
ALBUMS = {
        'rolling girls': 'https://movie.douban.com/subject/25955418/photos?type=S',
        '回转企鹅罐': 'https://movie.douban.com/subject/6085356/photos?type=S'
}

```

运行:
```
$ scrapy crawl douban_pic
```
