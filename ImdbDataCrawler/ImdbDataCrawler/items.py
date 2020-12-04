# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbdatacrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    release_date = scrapy.Field()
    duration = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    cast = scrapy.Field()
    summary = scrapy.Field()
    plot_keywords = scrapy.Field()
    genres = scrapy.Field()
    imdb_id = scrapy.Field()
