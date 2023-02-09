# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
import random

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/603-the-matrix']
    
    def parse(self, response):
        new_urls = response.url + '/cast'
        yield Request(new_urls, callback=self.parse_full_credits)
    
    def parse_full_credits(self, response):
        actor_urls = response.css('.pad:nth-child(1) .info a::attr(href)').getall()
        actor_urls = ["https://www.themoviedb.org" + url for url in actor_urls]
        for actor_url in actor_urls:
            yield Request(actor_url, callback=self.parse_actor_page)

    def parse_actor_page(self, response):
        
        actor_name = response.css(".title a::text").get()
        movies_and_tv_shows = response.css('.tooltip bdi::text').getall()
        for movie_or_tv_show in movies_and_tv_shows:
            yield {"actor": actor_name, "movie_or_TV_name": movie_or_tv_show}

            
    
        
