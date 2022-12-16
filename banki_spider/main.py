from scrapy.utils.project import get_project_settings
import jinja2
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess

from .banki_spider.pipelines import GetBanks
from .banki_spider.spiders import MortageSpider


def get_banks(price, initial_fee, is_have_child_before_2018, purpose_type, max_payment: int):
    banks = []
    for i in range(1, 10):
        MortageSpider.SetParameters(price, initial_fee, is_have_child_before_2018, purpose_type, i)
        process = CrawlerProcess(get_project_settings())
        d = process.crawl(MortageSpider.MortgageSpider)
        process.start()

        for bank in GetBanks():
            if bank['payment_per_mouth'] <= max_payment:
                banks.append(bank)

    banks.sort(key=lambda x: (x['period'], x['payment_per_mouth'], x['full_payment'], x['bank_name']))
    environment = jinja2.Environment()
    results_template = environment.get_template("banks.html")

    d.addBoth(lambda: reactor.stop())
    reactor.run()
    return results_template.render({'banks': banks})
