# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from whatclinicscraper.items import WhatclinicscraperItem
import requests
import json

class WhatclinicspiderSpider(scrapy.Spider):
    name = "whatclinicspider"
    allowed_domains = ["whatclinic.com"]
    start_urls = (
        'http://www.whatclinic.com/cosmetic-dentists/worldwide',
        'http://www.whatclinic.com/dentists/worldwide',
        'http://www.whatclinic.com/hair-loss/worldwide',
        'http://www.whatclinic.com/denturists/worldwide',
        'http://www.whatclinic.com/restorative-dentists/worldwide',
    )

    def parse(self, response):
        print response.url
        container_div = response.xpath('//div[@class="search-listing panel panel-default"]')

        for row in container_div:
            homepage_item = {}
            title_div = row.xpath('.//div[@class="section title-section rule-bottom"]')
            homepage_item["title"] = title_div.xpath('h3/a/text()').extract()
            homepage_item["url"] = title_div.xpath('h3/a/@href').extract()[0]
            homepage_item["phone"] = title_div.xpath('.//span[@property="telephone"]/text()').extract()
            homepage_item["country"] = title_div.xpath('.//span[@class="address"]/text()').extract()[1].split(",")
            homepage_item["longitude"] = title_div.xpath('.//span[@class="longitude"]/@content').extract()
            homepage_item["latitude"] = title_div.xpath('.//span[@class="latitude"]/@content').extract()
            homepage_item["image"] = row.xpath('.//div[@class="clinic-image"]/img/@src').extract()[0]

            url = response.urljoin(homepage_item["url"])
            req = Request(url=url, callback=self.parse_detail)
            req.meta['homepage_item'] = homepage_item
            yield req

    def parse_detail(self, response):
        homepage_item = response.meta['homepage_item']

        item = WhatclinicscraperItem()

        category = homepage_item["url"].split("/")[1]
        category = category.replace("-", " ")

        description_div = response.xpath(".//div[@property='description']")
        description = description_div.xpath("text()").extract()
        video = description_div.xpath(".//embed/@src").extract()
        tags = response.xpath(".//div[@class='treatment_body ']/h6/span/text()").extract()

        address = response.xpath('.//span[@property="address"]/text()').extract()[1]
        open_hours = response.xpath(".//div[@class='open_time']/@content").extract()

        country_name = homepage_item["country"][1]
        if country_name[:1] == " ":
            country_name = country_name[1:]

        if country_name[-1:] == " ":
            country_name = country_name[:-1]

        region_country_name = country_name
        if region_country_name == "Hong Kong SAR":
            region_country_name = "Hong Kong"

        region_url = "https://restcountries.eu/rest/v1/name/" + region_country_name + "?fullText=true"
        response_value = requests.get(region_url)
        #print region_url

        sub_region = ""
        if response_value.json()[0]:
            sub_region = response_value.json()[0]["subregion"]

        # if homepage_item["latitude"] and homepage_item["longitude"]:
        #     gmap_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + homepage_item["latitude"][0] + ","+ homepage_item["longitude"][0] + "&key=AIzaSyCQpO04eP4GVRzgVZqH6NWhW7Ugqt0PweY"
        #     response_value = requests.get(gmap_url)
        #     address_components = response_value.json()["results"][0]["address_components"]
        #     for row in address_components:
        #         print row


        item["post_id"] = ""
        item["post_title"] = homepage_item["title"][0]
        item["post_author"] = "admin"
        item["post_content"] = " ".join(description)
        item["post_category"] = category
        item["post_tags"] = ",".join(tags)
        item["post_type"] = "gd_hospitals"
        item["post_staus"] = "publish"
        item["geodir_video"] = video
        item["post_address"] = address
        item["post_city"] = homepage_item["country"][0]
        item["post_region"] = sub_region
        item["post_country"] = homepage_item["country"][1]
        item["post_latitude"] = homepage_item["latitude"][0]
        item["post_longitude"] = homepage_item["longitude"][0]
        item["geodir_timing"] = open_hours
        item["geodir_phoneno"] = homepage_item["phone"]
        item["IMAGE"] = homepage_item["image"].split("?")[0]

        item["post_zip"] = ""
        item["Neighbourhoods"] = ""
        item["geodir_contact"] = ""
        item["geodir_email"] = ""
        item["geodir_website"] = ""
        item["geodir_twitter"] = ""
        item["geodir_facebook"] = ""

        yield item
