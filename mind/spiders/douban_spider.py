# -*- coding: utf-8 -*-
import scrapy
from mind.items import MindItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        x = response.xpath("//ol[@class='grid_view']/li")
        for item in x:
            douban_item = MindItem()
            douban_item['movie_rank'] = item.xpath(".//em/text()").extract_first()
            douban_item['movie_name'] = item.xpath(".//span[@class='title']/text()").extract_first()
            douban_item['movie_score'] = item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['movie_describe'] = item.xpath(".//span[@class='inq']/text()").extract_first()
            douban_item['movie_pic'] = item.xpath(".//div[@class='pic']//img/@src").extract_first()
            #douban_item['movie_star'] = item.xpath(".//div[@class='star']/span[0]/@class").extract()
            #传递数据
            yield douban_item
            print(douban_item)


        next_link = response.xpath("//div[@class='paginator']//span[@class='next']//a/@href").extract()
        if next_link:
            next_url = self.start_urls[0] + next_link[0]
            yield scrapy.Request(next_url, callback=self.parse)


