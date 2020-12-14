# -*- coding: UTF-8 -*-
import html
import json
import scrapy
from ..items import SteamItem
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree
import requests


class ItcastSpider(scrapy.Spider):
    name = 'game'
    allowed_domains = ['store.steampowered.com']

    # 生成列表页url
    start_urls = []
    base_url = 'https://store.steampowered.com/search/?category1=998&page={}'

    # 获取要爬取的游戏总页数
    page_url = "https://store.steampowered.com/search/?category1=998&page=1"
    res = requests.get(url=page_url,
                       headers={'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"})
    tree = etree.HTML(res.text)
    xp = '//*[@id="search_result_container"]/div[4]/div[2]/a[3]'
    total_page = tree.xpath(xp)
    total_page = int(total_page[0].text)
    total_page += 1

    for page in range(1, total_page):
        start_urls.append(base_url.format(page))
        # break

    def parse(self, response):
        a_list = response.xpath('//*[@id="search_resultsRows"]/a')
        print(len(a_list))
        for a in a_list:
            item = SteamItem()
            # 统一设置默认值
            item["game_name"] = ''
            item["detail_url"] = ''
            item["release_date"] = ''
            item["publisher"] = ''
            item["developer"] = ''
            item["tags"] = ''
            item["game_price"] = ''
            item["game_review"] = ''
            item["info"] = ''
            item["imgs"] = ''
            item["review_list"] = ''

            detail_link = a.xpath('./@href').extract()[0]
            try:
                item["detail_url"] = detail_link
                game_name = a.xpath('./div[2]/div/span/text()').extract()[0]
                release_date = a.xpath('./div[2]/div[2]/text()').extract()[0]

                print(game_name)
                item["game_name"] = game_name
                item["release_date"] = release_date
                game_price = a.xpath('./div[2]/div[4]/div[2]/text()').extract()[0].strip()  # 如果是正常价格
                if not game_price:  # 看看是否是打折价格
                    game_price = a.xpath('./div[2]/div[4]/div[2]/span/strike/text()').extract()[0].strip()
                    price_discount = a.xpath('./div[2]/div[4]/div[1]/span/text()').extract()[0].strip()  # 如果有打折，提取折扣力度
                else:
                    price_discount = '-0%'
                item["game_price"] = game_price
                item["price_discount"] = price_discount
            except Exception as e:
                print('名字／发布时间／价格／折扣　缺失')
                print(e)
                print('detail_link', detail_link)
                item["game_price"] = "¥ 0"
                item["price_discount"] = '-0%'

            # cookies跳过成人内容验证
            cookies = {
                'wants_mature_content': '1',
                'birthtime': '883661322',
                'lastagecheckage': '1-January-1998',
            }
            # 请求详情页
            detail_request = scrapy.Request(
                url=detail_link,
                callback=self.detail_parse,
                headers={
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "User-Agent": str(UserAgent().random)
                },
                meta={"item": item, 'detail_link': detail_link},
                cookies=cookies,
            )
            yield detail_request

    def detail_parse(self, response):
        item = response.meta["item"]
        detail_link = response.meta["detail_link"]
        try:
            game_summary = response.xpath('//div[@class="game_description_snippet"]/text()').extract()[0].strip()
            game_img = response.xpath('//img[@class="game_header_image_full"]/@src').extract()[0]

            # 解决publisher和developer布局问题
            publisher_list = response.xpath(
                '(//div[@class="dev_row"]/div[@class="subtitle column"])[2]/following-sibling::div[1]/a')
            developer_list = response.xpath('//div[@id="developers_list"]/a')
            sels_list = response.xpath('//div[@class="glance_tags popular_tags"]/a')
            tags = ''
            developer = ''
            publisher = ''
            # print(len(sels_list))

            for sel in sels_list:
                text = sel.xpath('.//text()').extract()[0].strip()
                tags += text
                tags += " "
            # print(tags)

            for develop in developer_list:
                text = develop.xpath('.//text()').extract()[0].strip()
                developer += text
                developer += ", "
            developer = developer[:-2]
            # print(developer)

            for publish in publisher_list:
                text = publish.xpath('.//text()').extract()[0].strip()
                publisher += text
                publisher += ", "
            publisher = publisher[:-2]
            # print(publisher)

            item["publisher"] = publisher
            item["developer"] = developer
            item["tags"] = tags
            item["info"] = game_summary
            item["imgs"] = game_img
            game_review = response.xpath('//span[@class="nonresponsive_hidden responsive_reviewdesc"]/text()').extract()[0].strip()
            game_review = game_review[2:]
            item["game_review"] = game_review
        except Exception as e:
            print('简介／评论／图片　缺失')
            print(e)
            item["game_review"] = "无用户评测"

        # 临时
        yield item


'''
        # 生成评论页url
        try:
            game_id = re.search('https://store.steampowered.com/app/(\d+)/.*?', detail_link).group(1)
            review_url = "https://store.steampowered.com/appreviews/{}?filter=summary&language=schinese&l=schinese".format(game_id)

            # 请求评论页
            review_request = scrapy.Request(
                url=review_url,
                callback=self.review_parse,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
                },
                meta={"item": item},
            )

        except Exception as e:
            print('正则', detail_link)
            print(e)
            review_request = ''

        yield review_request

    def review_parse(self, response):
        item = response.meta["item"]
        review_list = []
        try:
            # 获取json数据中的html文本
            data = response.text
            data_dict = json.loads(data)
            data_html = html.unescape(data_dict["html"])

            # 　构建bs4对象
            soup = BeautifulSoup(data_html, 'lxml')
            div_list = soup.select('div[class="content"]')
            for div in div_list:
                review = div.get_text()
                rev = review.strip()
                if rev:
                    review_list.append(rev)
        except Exception as e:
            print('评论缺失，无法解析')
            print(e)

        item["review_list"] = review_list
        yield item '''
