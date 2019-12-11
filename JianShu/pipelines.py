# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import hashlib

class JianshuPipeline(object):
    def process_item(self, item, spider):
        # conn = pymysql.connect(host="192.", user="root", passwd="", db="")
        # conn = pymysql.connect(host="192.", user="root", passwd="", db="")
        # cursor = conn.cursor()
        # Title = self.replace_str(('').join(item['Title']))
        # Author = self.replace_str(('').join(item['Author']))
        # PublishTime = ('').join(item['PublishTime'])
        # Brief = self.replace_str(('').join(item['Brief']))
        # Url = ('').join(item['Url'])
        # Image_url = (';').join(item['Image_url'])
        # Content_html = self.replace_str(('').join(item['Content_html']))
        # Source = '简书'
        # # Language = 'cn'
        # Views = item['Views']
        # Comment_count = item['Comment_count']
        # Likes = item['Likes']
        # md5 = self.get_md5(Title)
        # InsertTime = self.replace_str(item['InsertTime'])
        # SearchKeywords = self.replace_str(('').join(item['SearchKeywords']))
        # print("简书文章储存。。。。。。。", Title)
        # sql = """insert into datasource_blog(Title, Brief, PublishTime, Comment_count, Views, Likes, Url, SearchKeywords, Image_url, Author, md5, Content_html, InsertTime, Source) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') ON duplicate KEY UPDATE MD5 = MD5""" % (
        #     Title, Brief, PublishTime, Comment_count, Views, Likes, Url, SearchKeywords, Image_url, Author, md5, Content_html,
        #     InsertTime, Source)
        # print("简书文章储存正在存入数据库。。。。。。。。。。。。")
        # cursor.execute(sql)
        # conn.commit()
        # conn.close()
        return item

    def get_md5(self, Title):
        str = Title
        hl = hashlib.md5()
        hl.update(str.encode(encoding='utf-8'))
        return hl.hexdigest()

    def replace_str(self, strs):
        strs = strs.replace("'", "\\\'")
        strs = strs.replace("''", "\\\'")
        strs = strs.replace('"', '\\"')
        strs = strs.replace(">", "\>")
        strs = strs.replace("“", "\\”")
        strs = strs.replace("\\\'", "")
        # strs = strs.replace("\\", "")
        return strs

