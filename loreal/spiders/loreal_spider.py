from scrapy import Spider,Request
from loreal.items import LorealItem

class LorealSpider(Spider):
    name = 'loreal_spider'
    allowed_domains = ['www.lorealparisusa.com']
    start_urls = ['https://www.lorealparisusa.com/products/skin-care/shop-all-products.aspx?size=20&page=1']

    def parse(self, response):
        n_pages_skincare = len(response.xpath('//div[@class="results-pagination"]/a').extract()) - 2
        n_pages_makeup = len(response.xpath('//div[@class="results-pagination"]/a')) - 2
        n_pages_haircare = 4

        skincare_urls = ['https://www.lorealparisusa.com/products/skin-care/shop-all-products.aspx?size=20&page={}'.format(x) for x in range(1, n_pages_skincare+1)]
        makeup_urls = ['https://www.lorealparisusa.com/products/makeup/shop-all-products.aspx?size=20&page={}'.format(x) for x in range(1, n_pages_skincare+1)]
        haircare_urls = ['https://www.lorealparisusa.com/products/hair-care/shop-all-products.aspx?size=20&page={}'.format(x) for x in range(1, n_pages_haircare+1)]
        result_urls = skincare_urls + makeup_urls + haircare_urls

        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)

    def parse_result_page(self, response):
        products = response.xpath('//div[@class="product-container"]')
        for product in products:
            # url
            try:
                url = 'https://www.lorealparisusa.com' + product.xpath('./a/@href').extract_first()
            except:
                continue

            # product name
            try:
                product_name = product.xpath('./div[@class="product-container__data"]/div/a/h3/text()').extract_first()
            except:
                product_name = None

            # product price
            try:
                product_price = product.xpath('./div[@class="product-container__actions"]/a/span/text()').extract_first()
            except:
                product_price = None

            yield Request(url=url, callback=self.parse_detail_page, meta ={'name': product_name, 'price': product_price})

    def parse_detail_page(self, response):
        name = response.meta['name']
        price = response.meta['price']

        # main category
        try:
            main_category = response.xpath('//span[@itemprop="name"]/text()').extract()[1]
        except:
            main_category = None

        # category
        try:
            category = response.xpath('//span[@itemprop="name"]/text()').extract()[3]
        except:
            category = None

        # rating
        try:
            rating = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
        except:
            rating = None

        # number of reviews
        try:
            num_reviews = response.xpath('//span[@itemprop="reviewCount"]/text()').extract_first()
        except:
            num_reviews = None
        
        item = LorealItem()
        item['name'] = name
        item['price'] = price
        item['rating'] = rating
        item['category'] = category
        item['num_reviews'] = num_reviews
        item['main_category'] = main_category

        yield item





