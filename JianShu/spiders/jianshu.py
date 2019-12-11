# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
from JianShu.items import JianshuItem
import json
from JianShu.userAgents import get_random_agent
import time
import datetime
import re
import requests
from lxml import etree
import urllib.request as request
from bs4 import BeautifulSoup
from JianShu.Get_keywork import get_keyword
class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    # allowed_domains = ['https://www.jianshu.com/']
    # start_urls = ['http://https://www.jianshu.com//']
    random_agent = '"' + get_random_agent() + '"'
    headers = {
        "authority":'www.jianshu.com',
        # "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'method':'POST',
        'accept':'application/json',
        'upgrade-insecure-requests':'1',
        "User-Agent": random_agent,
        'path':'/search/do?q=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&type=note&page=1&order_by=default'
    }



    def start_requests(self):
        # keyword = get_keyword()
        keyword = ['人工智能']
        for i in keyword:
            for j in range(1,5):
                word = ('').join(i)
                pages = j
                url = 'https://www.jianshu.com/search/do?q={}&type=note&page={}&order_by=default'.format(word, pages)
                print(url)
                headers = {
                    "authority": 'www.jianshu.com',
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                    "method": 'POST',
                    "accept": 'application/json',
                    "x-csrf-token": 'w4WZccOuZnXi/52zxgz2iB3wusXHEhp+x2DijDNBKLoRHAMUsGpoXf1irYsFPEMwk5kLY/361ddn5ta9lm8qgA==',
                    # "User-Agent": self.random_agent,
                    "path": '/search/do?q={}&type=note&page={}&order_by=default'.format(word, pages),
                    "origin":'https://www.jianshu.com',
                    "referer":'https://www.jianshu.com/search?q={}&page={}&type=note'.format(word, pages),
                    "accept-encoding":'gzip, deflate, br',
                    "cookie":'__yadk_uid=2z1r7gQKnjuefkromyrosN22nmsJw1mz; locale=zh-CN; read_mode=day; default_font=font2; _m7e_session_core=059e3455d807a70294069ebdd5ef1155; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22166209fb4b732b-00f6a07f6faa3c-8383268-2073600-166209fb4b870d%22%2C%22%24device_id%22%3A%22166209fb4b732b-00f6a07f6faa3c-8383268-2073600-166209fb4b870d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1575959868,1575959869,1576033114,1576033890; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1576033890; signin_redirect=https%3A%2F%2Fwww.jianshu.com%2Fsearch%3Fq%3D%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD%26page%3D1%26type%3Dnote'
                }
                # formdata = {
                #     'q': i,
                #     'type': 'note',
                #     'page': str(j),
                #     'order_by': 'default'
                # }
                # temp = json.dumps(formdata)
                yield scrapy.FormRequest(url,formdata={ 'q': i,
                        'type': 'note',
                        'page': str(j),
                        'order_by': 'default'},callback=self.parse, meta={"word":word, "pages":pages}, headers=headers, dont_filter=True)
                # yield scrapy.Request(url, body=temp, callback=self.parse, meta={"word":word, "pages":pages}, headers=headers, dont_filter=True)
    def parse(self, response):
        word = ('').join(response.meta['word'])
        word = "\'"+word+"\'"
        # print(word)
        pages = str(response.meta['pages'])
        pages = "\'"+pages+"\'"
        # print(pages)
        data = response.body
        print(data)
        log_info = '=========正在爬取{}文章,第{}页=========='.format(word,pages)
        print(log_info)
        data = json.loads(data)
        print(data)
        infos = data['entries']
        for i in infos:
            Title_origin = i['title']
            # Title = re.sub("[A-Za-z\<\>\-\=\''\/\ ]","",Title_origin)
            selector = etree.HTML(Title_origin)
            Title = ('').join(selector.xpath('//text()'))
            print('标题：',Title)
            user_info = i['user']['nickname']
            selector = etree.HTML(user_info)
            Author = ('').join(selector.xpath('//text()'))
            print('作者：',Author)
            slug = i['slug']
            Url = 'https://www.jianshu.com/p/' + slug
            print('原文链接：',Url)
            Brief_origin = i['content']
            selector = etree.HTML(Brief_origin)
            Brief = ('').join(selector.xpath('//text()'))
            print('简介：',Brief)
            Views = i['views_count']
            print('浏览量：',Views)
            Comment_count = i['public_comments_count']
            print('评论数量：',Comment_count)
            Likes = i['likes_count']
            print('喜欢数量：',Likes)
            Pubtime = i['first_shared_at']
            PublishTime = Pubtime[:10]
            print('发表时间：',PublishTime)
            yield Request(Url, callback=self.parse_detail,meta={"Title":Title, "Author":Author, "Brief":Brief, "Views":Views, "Comment_count":Comment_count, "Likes":Likes,"PublishTime":PublishTime, "Url":Url, "word":word},headers=self.headers,dont_filter=True)

    def parse_detail(self,response):
        item = JianshuItem()
        Title = response.meta['Title']
        Author = response.meta['Author']
        Brief = response.meta['Brief']
        Views = response.meta['Views']
        Comment_count = response.meta['Comment_count']
        Likes = response.meta['Likes']
        PublishTime = response.meta['PublishTime']
        Url = response.meta['Url']
        SearchKeywords = ('').join(response.meta['word'])
        SearchKeywords = SearchKeywords[1:-1]

        InsertTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res = requests.get(response.url, headers=self.headers, verify=False)
        soup = BeautifulSoup(res.content, 'lxml')
        # Content_html_origin = soup.find('div',class_='show-content-free')
        Content_html_origin = soup.find('article', class_='_2rhmJa')
        Content_html = Content_html_origin.prettify()
        # print('==================================',Content_html)
        if 'img' in Content_html:
            # print('first:',htmlContent)
            pattern = re.compile('src=(".*?")')  # 修改htm中img标签 格式
            img_tag_origin = pattern.findall(Content_html)
            # print(img_tag_origin)
            # print(type(img_tag_origin))
            img_tag_after = []

            for i in img_tag_origin:
                img_tag_after.append('"https://' + i.split('//')[1])
            print(img_tag_after)
            pa = re.compile('<img.*?>')
            ma = pa.findall(Content_html)
            gg = ''
            for f,origin_tag in zip(img_tag_after,ma):
                img_tag = '<img ' + 'src=' + "".join(f) + '/>'
                # gg = re.sub(g, img_tag, htmlContent)
                gg = Content_html.replace(origin_tag, img_tag)
                Content_html = gg
            Content_html = gg
            # print(Content_html)#处理图片大小
            # pattern_2 = re.compile(':(.*?px);')
            Content_html_final = re.sub(':(.*?px);', ': 2%;', Content_html)           #把所有图片px大小的换成2%
            Content_html_final = '<!DOCTYPE html>' + Content_html_final
            print('原文html:', Content_html_final)
            item['Author'] = Author
            item['Title'] = Title
            item['Url'] = Url
            item['PublishTime'] = PublishTime
            item['Comment_count'] = Comment_count
            item['Likes'] = Likes
            item['Views'] = Views
            item['Brief'] = Brief
            item['Content_html'] = Content_html_final
            item['InsertTime'] = InsertTime
            item['SearchKeywords'] = SearchKeywords
            item['Image_url'] = img_tag_after
            yield item
        else:
            Content_html = Content_html
            print('原文html:', Content_html)
            img_tag_after = ''
            item['Author'] = Author
            item['Title'] = Title
            item['Url'] = Url
            item['PublishTime'] = PublishTime
            item['Comment_count'] = Comment_count
            item['Likes'] = Likes
            item['Views'] = Views
            item['Brief'] = Brief
            item['Content_html'] = Content_html
            item['InsertTime'] = InsertTime
            item['SearchKeywords'] = SearchKeywords
            item['Image_url'] = img_tag_after
            yield item