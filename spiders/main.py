# -*- coding: utf-8 -*-
import scrapy
import logging


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['www.yellowpages.com']
    start_urls = ['https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=New+York%2C+NY']

    def parse(self, response):
        lists = response.xpath('//div[@class="v-card"]')
        for each in lists:
            link = each.xpath('.//h2[@class="n"]/a/@href').get()
            yield response.follow(url=link, callback=self.parse_links)
        
        next_page = response.xpath('//a[@class="next ajax-page"]/@href').get()
        if next_page:
            yield response.follow(response.urljoin(url=next_page), callback=self.parse)

    def parse_links(self, response):
        link = response.url
        name = response.xpath('//div[@class="sales-info"]/h1/text()').get()
        address = response.xpath('//h2[@class="address"]/text()').get()
        website = response.xpath('//a[@class="primary-btn website-link"]/@href').get()
        phone = response.xpath('//p[@class="phone"]/text()').get()
        email = response.xpath('(//a[@class="email-business"])[1]/@href').get()

        yield {
            "Link": link,
            "Name": name,
            "Address": address,
            "Website": website,
            "Phone": phone,
            "Email": email,
        }