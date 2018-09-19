# -*- coding: utf-8 -*-
import scrapy
from dilidili.items import DilidiliItem
from urllib import parse
import re
base_url = 'http://www.dilidili.wang'

class DilidiliSpider(scrapy.Spider):
    name = 'dilidili_spider'
    allowed_domains = ['dilidili.wang']
    start_urls = ['http://www.dilidili.wang']

    def parse(self, response):
        initials_url_list = \
            response.xpath('//section[@class="cross"]//div[@class="type"]//a[text() = "A"]/parent::div/a/@href')
        for initials in initials_url_list:
            initials_url = base_url + initials.extract()
            request = scrapy.Request(initials_url, callback=self.parse_anime)
            yield request

        # pass

    def parse_anime(self, response):

        responseURL = response.url
        # requestURL = response.meta['url']

        # yield scrapy.Request(url=requestURL, headers=headers, meta={'url': requestURL}, callback=self.parse)

        anime_list = response.xpath('//div[@class="anime_list"]//dd//h3/a/@href')
        for anime_url in anime_list:
            # request = scrapy.Request(anime_url.extract, headers=headers, meta={'url': requestURL}, callback=self.parse_anime_info)
            request = scrapy.Request(anime_url.extract(), callback=self.parse_anime_info)
            yield request

        # pass

    def parse_anime_info(self, response):
        url = response.url
        item = DilidiliItem()
        anime_info = response.xpath('//div[@class="detail con24 clear"]//dl//dd')
        item['anime_name'] = anime_info.xpath('//h1/text()').extract()
        item['anime_region'] = anime_info.xpath(
            '//div[@class="d_label"]//b[text() = "地区："]/parent::div/a/text()').extract()
        item['anime_year'] = anime_info.xpath(
            '//div[@class="d_label"]//b[text() = "年代："]/parent::div/a/text()').extract()
        item['anime_year_second'] = anime_info.xpath(
            '//div[@class="d_label"]//b[text() = "年代："]/parent::div/text()').extract()
        anime_tag_list = anime_info.xpath('//div[@class="d_label"]//b[text() = "标签："]/parent::div/a/text()')
        anime_tag = ''
        # for i in anime_tag_list:
        # anime_tag += i.extract()
        anime_tag = "|".join(str(i.extract()) for i in anime_tag_list)
        # anime_tag += '|'
        item['anime_tag'] = anime_tag
        anime_company_list = anime_info.xpath('//div[@class="d_label"]//b[text() = "制作："]/parent::div/a/text()')
        anime_company = "|".join(str(i.extract()) for i in anime_company_list)
        item['anime_company'] = anime_company
        item['anime_status'] = anime_info.xpath(
            '//div[@class="d_label"]//b[text() = "状态："]/parent::div/text()').extract()
        anime_cast_list = anime_info.xpath('//div[@class="d_label2"]//b[text() = "声优："]/parent::div/a/text()')
        anime_cast = "|".join(str(i.extract()) for i in anime_cast_list)
        item['anime_cast'] = anime_cast
        item['anime_view'] = anime_info.xpath(
            '//div[@class="d_label2"]//b[text() = "看点："]/parent::div/text()').extract()
        item['anime_url'] = anime_info.xpath('//div[@id="content1"]/a/@data-url').extract()
        anime_set_number = response.xpath('//div[@class="container clear"]//div[@class="clear"]//'
                                          'div[@class="aside_cen2"]//div[@class="con24 m-10 xf_news"]//'
                                          'div[@class="time_pic list"]//div[@class="time_con"][1]//'
                                          'div[@class="swiper-wrapper mb20"]//a/@href').extract()
        item['anime_set_number'] = len(anime_set_number)
        yield item

