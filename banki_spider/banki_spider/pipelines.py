import dataclasses


BANKS = []


@dataclasses.dataclass
class Bank:
    bank_name: str
    rate: float
    payment_per_mouth: int
    period: int
    full_payment: int


def GetBanks():
    return BANKS


class BankiSpiderPipeline:
    def open_spider(self, spider):
        BANKS = []
        print('start_spider')

    def process_item(self, item, spider):
        bank_item = Bank(
            item['bank'],
            float(item['mortgage_rate']),
            int(item['payment'].replace(' ', '')),
            item['period'],
            item['period'] * 12 * int(item['payment'].replace(' ', ''))
        )
        BANKS.append(bank_item)
        print('proccess')
        return item
