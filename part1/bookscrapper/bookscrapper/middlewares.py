# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BookscrapperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BookscrapperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
        
        
from urllib.parse import urlencode
from random import randint
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class FakeUserAgentsMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
    
        self.scrapeops_api_key = os.getenv('SCRAPE_OPS_API_KEY')
        self.scrapeops_endpoint = os.getenv('SCRAPE_OPS_USER_AGENT_URL')
        self.scrapeops_fake_user_agent_enabled = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED')
        print(self.scrapeops_api_key)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULT')
        self.user_agents_list = []
        self.get_user_agents_list()
        self.scrapeops_fake_user_agents_enabled()  
    
    def get_user_agents_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get('result', [])
        print("****** USER AGENTS API CALLED*********")
        print(self.user_agents_list)
    
    def get_random_user_agent(self):
        random_index = randint(0, len(self.user_agents_list)-1)
        return self.user_agents_list[random_index]
    
    def scrapeops_fake_user_agents_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_endpoint is None or self.scrapeops_endpoint == '' :
            self.scrapeops_fake_user_agent_enabled = False
        else:
            self.scrapeops_fake_user_agent_enabled = True
    
    def process_request(self, request, spider):
        random_user_agent = self.get_random_user_agent()
        request.headers['User-Agent'] = random_user_agent
        
        print("*********** NEW HEADER ATTACHED *********")
        print(request.headers['User-Agent'])
        
class FakeHeadersMiddleware:
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
        self.scrapeops_api_key = os.getenv('SCRAPE_OPS_API_KEY')
        self.scrapeops_endpoint = os.getenv('SCRAPE_OPS_HEADERS_URL')
        self.scrapeops_headers_enabled = settings.get('SCRAPEOPS_FAKE_HEADERS_ENABLED')
        print(self.scrapeops_api_key)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULT')
        self.headers_list = []
        self.header_parameters = ["upgrade-insecure-requests","user-agent","accept","sec-ch-ua","sec-ch-ua-mobile","sec-ch-ua-platform","sec-fetch-site","sec-fetch-mod","sec-fetch-user","accept-encoding","accept-language"]
        self.get_headers_list()
        self._scrapeops_headers_enabled()  
        
    def get_headers_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])
        print("****** HEADERS API CALLED*********")
        print(self.headers_list)
    
    def get_random_headers(self):
        random_index = randint(0, len(self.headers_list)-1)
        return self.headers_list[random_index]
    
    def _scrapeops_headers_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_endpoint is None or self.scrapeops_endpoint == '' :
            self.scrapeops_headers_enabled = False
        else:
            self.scrapeops_headers_enabled = True
    
    def process_request(self, request, spider):
        random_headers = self.get_random_headers()
        print("*********** NEW HEADER ATTACHED *********")
        for header in self.header_parameters:
            request.headers[header] = random_headers[header]
        print(request.headers)

## IF I HAD SMART PROXY SUBSCRIPTION, THIS WOULD HAVE BEEN IDEAL

# import base64

# class MyProxyMiddleware:
    
#     @classmethod
#     def from_crawl(cls, crawler):
#         return cls(crawler.settings)
    
#     def __init__(self, settings):
#         self.proxy_username = os.getenv('SMART_PROXY_USERNAME')
#         self.proxy_password = os.getenv('SMART_PROXY_PASSWORD')
#         self.proxy_auth_token = os.getenv('SMART_PROXY_AUTH_TOKEN')
#         self.proxy_endpoint = os.getenv('SMART_PROXY_ENDPOINT')
#         self.port = os.getenv('SMART_PROXY_PORT')
        
#     def process_request(self, request, spider):
#         user_credentials = f'{self.proxy_username}:{self.proxy_password}'
#         basic_authentication = 'Basic '+ base64.b64encode(user_credentials.encode()).decode()
#         host = f'http://{self.proxy_endpoint}:{self.port}'
#         request.meta['proxy'] = host
#         request.headers['Proxy-Authorization'] = basic_authentication
#         print("****BASIC AUTH****", basic_authentication)
#         print("****PROXY HOST****", host)
        
        
        
        