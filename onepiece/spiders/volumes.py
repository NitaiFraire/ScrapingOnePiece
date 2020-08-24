import scrapy


class VolumesSpider(scrapy.Spider):
    name = 'volumes'
    start_urls = ['https://onepiece.fandom.com/wiki/Volume_1']

    def parse(self, response):
        volume = response.xpath("//aside//section")
        n_volume = response.xpath("//h1[@class='page-header__title']/text()").get()
        n_volume = n_volume.split(' ')[1]
        cover = response.xpath("//aside//figure/a/@href").get()
        if not cover:
            cover = response.xpath("//aside//span[1]/a/@href").get()
        release_date = volume.xpath(".//div[@data-source='date']/div/text()[1]").get()
        release_date_year = volume.xpath(".//div[@data-source='date']/div/a/text()").get()
        if release_date_year:
            release_date += release_date_year
        release_date = release_date.split(' (')[0]
        yield { 
            'volume': n_volume,
            'title': response.xpath("//aside/h2/text()").get(),
            'cover': cover,
            'chapters': volume.xpath(".//div[@data-source='chapters']/div/text()").get(),
            'release_date': release_date
        }
        next_volume = response.urljoin(response.xpath("//aside//table//td[2]/a/@href").get())
        if next_volume is not None:
            yield response.follow(next_volume, callback=self.parse)
