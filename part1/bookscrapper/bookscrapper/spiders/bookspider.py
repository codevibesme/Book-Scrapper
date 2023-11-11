from typing import Iterable
import scrapy
from scrapy.http import Request
from bookscrapper.items import BookItem
from dotenv import load_dotenv
import os
from urllib.parse import urlencode
load_dotenv()

def get_proxy_url(url):
    payload = {'api_key': os.getenv('SCRAPE_OPS_API_KEY'), 'url': url}
    proxy_url = f'{os.getenv('SCRAPE_OPS_PROXY_ENDPOINT')}?{urlencode(payload)}'
    print("***PROXY URL****", proxy_url)
    return proxy_url

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com", "proxy.scrapeops.io"]
    start_urls = ["https://books.toscrape.com"]
    
    def start_requests(self):
        yield scrapy.Request(url=get_proxy_url(self.start_urls[0]), callback=self.parse)
        # yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse_book_details(self, response):
        table_rows = response.css('table tr')
        rating = response.css('p.star-rating').attrib['class']
        stars = rating[(rating.find(' ')+1):]
        
        book_item = BookItem()
        
        book_item['url'] =  response.url
        book_item['title'] = response.css('h1 ::text').get()
        book_item['product_type'] =  table_rows[1].css("td ::text").get()
        book_item["price_incl_tax"] =  table_rows[3].css("td ::text").get()
        book_item['price'] = response.css('p.price_color ::text').get()
        book_item["tax"] =  table_rows[4].css("td ::text").get()
        book_item['num_reviews'] =  table_rows[6].css("td ::text").get()
        book_item['stars'] =  stars,
        book_item['category'] =  response.xpath('/html/body/div/div/ul/li[3]/a/text()').get()
        book_item['description'] =  response.xpath('/html/body/div/div/div[2]/div[2]/article/p/text()').get()
        
        yield book_item

    def parse(self, response):
        books = response.css('article.product_pod')
        book_url=''
        for book in books:
            product_url = book.css('h3 a ::attr(href)').get()
            if 'catalogue/' in product_url:
                book_url = "https://books.toscrape.com/"+product_url
            else:
                book_url = "https://books.toscrape.com/catalogue/"+product_url
                
            yield response.follow(get_proxy_url(book_url), callback = self.parse_book_details)
            # yield response.follow(book_url, callback = self.parse_book_details)
        next_page = response.css('li.next a ::attr(href)').get()
        
        if next_page is not None:
            page_no = next_page[next_page.find("page"):]
            next_page_url = 'https://books.toscrape.com/catalogue/' + page_no
            yield response.follow(get_proxy_url(next_page_url), callback = self.parse)
            # yield response.follow(next_page_url, callback = self.parse)
