import scrapy
import os
from ..constants import Constants


class AllGenreSpider(scrapy.Spider):
    name = "all_genre"
    start_urls = [
        f"{Constants.DOMAIN_NAME.value}/feature/genre/?ref_=nv_ch_gr",
    ]

    def parse(self, response, **kwargs):
        genre_links = response.css(".aux-content-widget-2:nth-child(8)").css("a::attr(href)").extract()
        os.makedirs(os.path.dirname(Constants.ALL_GENRE_DUMP.value), exist_ok=True)
        yield
        with open(Constants.ALL_GENRE_DUMP.value, "w+") as f:
            for link in genre_links:
                # print(link.css("a::text").extract())
                f.write(f"{link}\n")
                yield
