import scrapy
import urllib.parse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from ..items import TutorialItem

class IndiamartAPISpider(scrapy.Spider):    
    name = "indiamart_api"
    allowed_domains = ["dir.indiamart.com"]

    async def start(self):
        query = "industry machinery"
        city = "bengaluru"

        # URL encode query and city
        query_enc = urllib.parse.quote_plus(query)
        city_enc = urllib.parse.quote_plus(city)

        url = f"https://dir.indiamart.com/search.mp?ss={query_enc}&cq={city_enc}&pg=1"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/127.0.0.0 Safari/537.36",
            "Accept": "application/json,text/html;q=0.9",
        }

        yield scrapy.Request(url, headers=headers, callback=self.parse, meta={"pg": 1, "query": query, "city": city})

    def parse(self, response):
        products = response.css(".brs5")  # each product card
        uri = "mongodb+srv://dionclivesaldanha22ds:VJA6iUEtGSbpYmgA@cluster0.yfwll51.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri, server_api=ServerApi('1'))

        db = client.product_db
        prod = db.products

        for p in products:
            product_items = TutorialItem()
            
            # Extract fields with defaults
            product_items['name'] = p.css(".elps2 .cardlinks::text").get(default="N/A")
            product_items['price'] = p.css(".price::text").get(default="₹ 0")
            product_items['company'] = p.css(".cardlinks.elps1::text").get(default="N/A")
            product_items['location'] = p.css(".newLocationUi .highlight::text").get(default="N/A")
            product_items['address'] = p.css(".newLocationUi p::text").get(default="N/A")
            
            link = p.css(".elps2 .cardlinks::attr(href)").get()
            if link:
                product_items['product_link'] = response.urljoin(link)
            else:
                product_items['product_link'] = ""

            # Insert into MongoDB one by one
            # prod.insert_one(dict(product_items))

            yield product_items  # still yielding to pipelines/logging if needed

        # --- Pagination Logic ---
        current_page = response.meta["pg"]
        query = response.meta["query"]
        city = response.meta["city"]

        if current_page < 5:
            next_page = current_page + 1
            query_enc = urllib.parse.quote_plus(query)
            city_enc = urllib.parse.quote_plus(city)
            next_url = f"https://dir.indiamart.com/search.mp?ss={query_enc}&cq={city_enc}&pg={next_page}"
            yield scrapy.Request(next_url, callback=self.parse, meta={"pg": next_page, "query": query, "city": city})
# why its only fecthing 51 results