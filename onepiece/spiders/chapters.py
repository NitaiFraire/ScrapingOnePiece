import scrapy


class ChaptersSpider(scrapy.Spider):
    name = 'chapters'
    start_urls = ['http://onepiece.fandom.com/wiki/Chapter_1']

    def parse(self, response):
        chapter = response.xpath("//h1[@class='page-header__title']/text()").get().split()[1]
        volume = response.xpath("//aside//section/div[@data-source='vol']/div/text()").get()
        title = response.xpath("//aside/h2/text()").get()
        if not title:
            title = response.xpath("//aside/h2/b/text()")
        cover = response.xpath("//aside//figure/a/@href").get()
        pages = response.xpath("//aside//section/div[@data-source='page']/div/text()").get()
        release_date = response.xpath("//aside//section/div[@data-source='date2']/div/text()").get()
        yield {
            'chapter': chapter,
            'volume': volume,
            'title': title,
            'cover': cover,
            'pages': pages,
            'release_date': release_date
        }
        next_chapter = response.xpath("//aside//section[2]//td[2]/a/@href").get()
        if next_chapter is not None:
            yield response.follow(next_chapter, callback=self.parse)

