import scrapy


class BankiSpiderItem(scrapy.Item):
    bank = scrapy.Field()
    mortgage_rate = scrapy.Field()
    payment = scrapy.Field()
    period = scrapy.Field()
