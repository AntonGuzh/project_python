from scrapy.utils.project import get_project_settings
import jinja2
from scrapy.crawler import CrawlerRunner

from .banki_spider.pipelines import GetBanks
from .banki_spider.spiders import MortageSpider


def get_banks(price, initial_fee, is_have_child_before_2018, purpose_type, max_payment: int):
    banks = []
    print('aaaaa')
    MortageSpider.SetParameters(price, initial_fee, is_have_child_before_2018, purpose_type)
    process = CrawlerRunner(get_project_settings())
    process.crawl(MortageSpider.MortgageSpider)
    process.start()

    print(price, initial_fee, is_have_child_before_2018, purpose_type, max_payment)
    for bank in GetBanks():
        if bank.payment_per_mouth <= max_payment:
            banks.append(bank)

    banks.sort(key=lambda x: (x.period, x.payment_per_mouth, x.full_payment, x.bank_name))
    with open("banks.html", encoding="UTF-8") as f:
        template_str = f.read()
    template = jinja2.Environment(loader=jinja2.FileSystemLoader(".")).from_string(template_str)
    html_str = template.render(banks=banks)

    return html_str

# print(get_banks(5_000_000, 2_000_000, 1, 'new', 20_000))
