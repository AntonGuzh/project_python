import scrapy
from urllib.parse import urlencode
from ..items import BankiSpiderItem


PAYLOAD = {
    'initialFee': 3000000,          # первоначальный взнос
    'price': 5000000,               # цена жилья
    'period': 1,                    # период выплаты (класс)
    'isHaveChildBefore2018': 0,     # имеется ли ребенок рожденный после 2018
    'purposeIds[]': 1,
    'specialProgramIds[]': -1,
}

PERIODS = {
    1: 1,
    2: 2,
    3: 4,
    4: 5,
    5: 10,
    6: 15,
    7: 20,
    8: 25,
    9: 30,
}


def SetParameters(price, initial_fee, is_have_child_before_2018, purpose_id, period):
    global PAYLOAD
    PAYLOAD['price'] = price
    PAYLOAD['initialFee'] = initial_fee
    PAYLOAD['period'] = period
    PAYLOAD['isHaveChildBefore2018'] = 1 if is_have_child_before_2018 else 0
    PAYLOAD['purposeIds[]'] = 2 if purpose_id == 'new' else 1


class MortgageSpider(scrapy.Spider):
    name = 'MortgageSpider'
    allowed_domains = ['banki.ru']

    def __init__(self):
        super().__init__()
        self.start_urls = ['https://www.banki.ru/products/hypothec/search/moskva/?' + urlencode(PAYLOAD)]

    def parse(self, response):
        bank_items = response.xpath('//table//tr/td/text()').extract()
        for i in range(5, len(bank_items), 8):
            item = BankiSpiderItem()
            item['bank'] = bank_items[i].replace('\n', '').replace('\t', '').strip()
            item['mortgage_rate'] = bank_items[i + 1].replace('\n', '').replace('\t', '').replace(' %', '')\
                .replace(',', '.').strip()
            item['payment'] = bank_items[i + 2].replace('\n', '').replace('\t', '').replace(' ₽', '').strip()
            item['period'] = PERIODS[PAYLOAD['period']]
            yield item
