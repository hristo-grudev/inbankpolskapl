import scrapy

from scrapy.loader import ItemLoader
from ..items import InbankpolskaplItem
from itemloaders.processors import TakeFirst


class InbankpolskaplSpider(scrapy.Spider):
	name = 'inbankpolskapl'
	start_urls = ['https://www.inbankpolska.pl/warto-wiedziec/aktualnosci/',
	              'https://www.inbankpolska.pl/warto-wiedziec/blog/'
	              ]

	def parse(self, response):
		post_links = response.xpath('//article/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@aria-label="Next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h4/text()').get()
		description = response.xpath('//div[@class="text-justified"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=InbankpolskaplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
