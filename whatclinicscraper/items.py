# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WhatclinicscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    post_id = scrapy.Field()
    post_title = scrapy.Field()
    post_author = scrapy.Field()
    post_content = scrapy.Field()
    post_category = scrapy.Field()
    post_tags = scrapy.Field()
    post_type = scrapy.Field()
    post_staus = scrapy.Field()
    geodir_video = scrapy.Field()
    geodir_video = scrapy.Field()
    post_address = scrapy.Field()
    post_city = scrapy.Field()
    post_region = scrapy.Field()
    post_country = scrapy.Field()
    post_zip = scrapy.Field()
    post_latitude = scrapy.Field()
    post_longitude = scrapy.Field()
    Neighbourhoods = scrapy.Field()
    geodir_timing = scrapy.Field()
    geodir_contact = scrapy.Field()
    geodir_email = scrapy.Field()
    geodir_phoneno = scrapy.Field()
    geodir_website = scrapy.Field()
    geodir_twitter = scrapy.Field()
    geodir_facebook = scrapy.Field()
    IMAGE = scrapy.Field()
