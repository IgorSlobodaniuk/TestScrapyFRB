from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail

class HasProperTitleContract(Contract):
    """ Demo contract which checks a title
        @is_in_title 'Foreign Exchange Rates'
    """

    name = 'is_in_title'

    print 7777777777777777777777777777777777777777

    def pre_process(self, response):
        title = response.xpath('.//title/text()').extract_first()
        for i in self.args:
            print 56565656565656565
            if i not in title:
                raise ContractFail('Incorrect title')
