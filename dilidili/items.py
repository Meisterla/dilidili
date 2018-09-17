# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DilidiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    anime_name = scrapy.Field()
    anime_region = scrapy.Field()
    anime_year = scrapy.Field()
    anime_year_second = scrapy.Field()
    anime_tag = scrapy.Field()
    anime_view = scrapy.Field()
    anime_company = scrapy.Field()
    anime_cast = scrapy.Field()
    anime_status = scrapy.Field()
    anime_url= scrapy.Field()

    #pass
