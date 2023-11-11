# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscrapperPipeline:
    def process_item(self, item, spider):
        print("ITEMMMMM")
        print(item)
        adapter = ItemAdapter(item)
        
        field_names = adapter.field_names()
        # Strip all whitespaces from strings except for description
        for field_name in field_names:
            if field_name != 'description' or field_name !='title':
                if field_name == 'stars':
                    value = adapter.get(field_name)[0].strip()
                else:
                    value = adapter.get(field_name).strip()
                adapter[field_name] = value.strip()
        
        #Category & Product type --> Switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()
            
        ##Price -->converter to float
        price_keys = ['price', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            print("*****")
            print(value)
            adapter[price_key] = float(value)
        
        #Converting num reviews to integer
        num_reviews = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews)
        
        stars = adapter.get('stars').lower().strip()
        star_keys = {
            'zero': 0,
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9,
        }
        adapter['stars'] = star_keys[stars]
        
        return item
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
load_dotenv()

class SaveToDB:
    
    def __init__(self):
        print("HIIII FROM DB")
        self.uri = os.getenv("MONGO_URL")
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        try:
            self.client.admin.command("ping")            
            print("Connection to DB successfull")
            self.db = self.client["books"]
        except Exception as e:
            print("******DB ERROR***********")
            print(e)
        
        
    def process_item(self, item, spider):
        print("*********ITEM********")
        print(dict(item))
        print(self.db)
        try:
            result = self.db.book.insert_one(dict(item))
            print("SUCCESFULLY SAVED:", result)
        except Exception as e:
            print("FAILED TO SAVE AT DB: ",e)
        return item
    
    def close_spider(self, spider):
        self.client.close()
        print("Closed Server");