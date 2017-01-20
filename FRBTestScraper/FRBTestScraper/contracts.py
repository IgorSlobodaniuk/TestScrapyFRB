from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail

class HasProperTitleContract(Contract):
    """ Demo contract which checks a title
        @is_in_title 'Foreign Exchange Rates'
    """

    name = 'is_in_title'

    def pre_process(self, response):
        title = response.xpath('.//title/text()').extract_first()
        for i in self.args:
            if i not in title:
                raise ContractFail('Incorrect title')
