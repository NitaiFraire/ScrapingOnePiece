# -*- coding: utf-8 -*-
import scrapy


class ArcsSpider(scrapy.Spider):
    name = 'arcs'
    allowed_domains = ['onepiece.fandom.com']
    start_urls = ['https://onepiece.fandom.com/wiki/Romance_Dawn_Arc']

    def parse(self, response):
        arc = response.xpath("//aside/section")
        years_released = arc.xpath(".//div[@data-source='date']/div/text()").get()
        years_released = years_released.split('(')[0]
        yield {
            'title': arc.xpath(".//h2/text()").get(),
            'cover': response.xpath("//aside/figure/a/@href").get(),
            'volumes': arc.xpath(".//div[@data-source='vol']/div/text()").get(),
            'chapters': arc.xpath(".//div[@data-source='chapter']/div/text()").get(),
            'years_released': years_released
        }
        next_arc = response.urljoin(response.xpath("//aside//table//td[@data-source='next']/a/@href").get())
        if next_arc:
            yield scrapy.Request(url=next_arc, callback=self.parse)

