# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    game_name = scrapy.Field() #游戏名称
    detail_url = scrapy.Field() #详情页链接
    release_date = scrapy.Field() #发行日期
    publisher = scrapy.Field() #发行商
    developer = scrapy.Field() #开发商
    tags = scrapy.Field() #游戏标签
    game_review = scrapy.Field() #游戏好评率
    game_price = scrapy.Field()#游戏原价
    info = scrapy.Field()#游戏简介
    imgs = scrapy.Field()#游戏图片
    review_list = scrapy.Field()#玩家评价
    price_discount = scrapy.Field()#打折折扣
