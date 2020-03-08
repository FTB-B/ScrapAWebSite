# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
#Extract data in temporary container(items)
import scrapy


class DonalwinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    post_1title = scrapy.Field()
    post_2href = scrapy.Field()
    post_3author = scrapy.Field()
    post_4vote = scrapy.Field()
    post_5time = scrapy.Field()
    post_6total_comments = scrapy.Field()
    post_7comments = scrapy.Field()
    #pass
