# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()  # 题目
    Author = scrapy.Field()  # 作者
    Brief = scrapy.Field()  # 摘要
    Content = scrapy.Field()  # 内容
    PublishTime = scrapy.Field()  # 发表时间
    SearchKeywords = scrapy.Field()  # 关键词
    Source = scrapy.Field()  # 来源
    Url = scrapy.Field()  # 文章url
    Views = scrapy.Field()  # 浏览数
    Image_url = scrapy.Field()  # 文章正文內容中的圖片链接
    Content_html = scrapy.Field()  # 文章正文内容html
    Comment_count = scrapy.Field()
    Likes = scrapy.Field()
    InsertTime = scrapy.Field()
    pass
