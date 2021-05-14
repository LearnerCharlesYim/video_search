# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParkItem(scrapy.Item):
    name = scrapy.Field()#名字
    author = scrapy.Field()#作者
    city = scrapy.Field()
    hot = scrapy.Field()
    day = scrapy.Field()
    url = scrapy.Field()



