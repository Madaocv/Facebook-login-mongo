# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
#scrapy crawl face -a login=ucantdream@gmail.com -a password=ZXCVBNM1234567890 -o person.json
connection = MongoClient() 
db = connection.trump

class FaceSpider(scrapy.Spider):
    name = "face"
    allowed_domains =["facebook.com"]
    start_urls = ['https://www.facebook.com/']

    def __init__(self, login = None, password = None, *args, **kwargs):
        super(FaceSpider, self).__init__(*args, **kwargs)
        self.login = login
        self.password = password

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formxpath='//form[contains(@action, "login")]',
            formdata={
                'email': self.login,
                'pass': self.password,
            },
            callback=self.parse_logged,
        )
    def parse_logged(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formxpath='//form[contains(@action, "search")]',
            formdata={
                'q': 'Donald J. Trump',
            },
            callback=self.parse_search,
        )
    def parse_search(self, response):
        peple_search_link = response.xpath("//a[contains(@href, '/search/pages/')]/@href").extract()
        return scrapy.Request(response.urljoin(peple_search_link[0]),  callback=self.parse_list)
    
    def parse_list(self, response):
        body = response.body.replace('<!--','').replace('-->','')
        response = response.replace(body=body)
        for a in response.xpath("//a[@data-testid and not(@aria-hidden)]")[1:]:
            item = {}
            item['name'] = a.xpath('div/text()').extract()[0]
            item['href'] = a.xpath('@href').extract()[0]
            #db.person.insert_one(item)
            #yield item