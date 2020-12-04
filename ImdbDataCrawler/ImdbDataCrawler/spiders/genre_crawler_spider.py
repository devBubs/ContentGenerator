import scrapy
from ..constants import Constants
from ..items import ImdbdatacrawlerItem
from ..pipelines import ImdbdatacrawlerPipeline


class GenreCrawlerSpider(scrapy.Spider):
    name = "genre_crawler"
    custom_settings = {'ITEM_PIPELINES': {'ImdbDataCrawler.pipelines.ImdbdatacrawlerPipeline': 300}}
    start_urls = []
    page_count = 0
    for url in open(Constants.ALL_GENRE_DUMP.value, "r"):
        url_strip = url.replace('\n', '')
        start_urls.append(f"{Constants.DOMAIN_NAME.value}{url_strip}")

    def parse(self, response, **kwargs):
        movie_link_list = response.css(".lister-item-header").css("a::attr(href)").extract()
        for movie_link in movie_link_list:
            # if GenreCrawlerSpider.movie_count == 2:
            #     break
            # GenreCrawlerSpider.movie_count += 1
            yield scrapy.Request(f"{Constants.DOMAIN_NAME.value}/{movie_link}", callback=self.parse_movie)
        next_page = response.css("a.next-page::attr(href)").get()
        print(f"Next page link: {next_page}")
        # GenreCrawlerSpider.page_count += 1
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_movie(self, response):
        try:
            item = ImdbdatacrawlerItem()
            item["imdb_id"] = response.css(".poster").css("a::attr(href)").get().split("/")[2]
            # getting title
            item['title'] = response.css(".title_wrapper").css("h1::text").get().replace('\xa0', '')
            # getting genres
            subtext = response.css(".title_wrapper").css("div.subtext").css("a::text").extract()
            item['genres'] = subtext[:-1]
            # getting release date
            item['release_date'] = subtext[-1].split("(")[0].rstrip(" ")
            # getting duration
            item['duration'] = response.css(".title_wrapper").css("div.subtext").css("time::text").get().strip()
            # getting director
            credit_summary_items = response.css(".credit_summary_item")
            item["directors"] = credit_summary_items[0].css("a::text").extract()
            # getting writers
            writer_selectors = credit_summary_items[1].css("a")
            item['writers'] = []
            for ws in writer_selectors:
                if ws.css("a::attr(href)").get().startswith("/name"):
                    item['writers'].append(ws.css("a::text").get())
            # getting cast
            cast_table = response.css(".primary_photo")
            item['cast'] = []
            for cell in cast_table:
                item['cast'].append(cell.css("a").css("img::attr(alt)").get())
            # getting summary and plot keywords
            title_story_line_block = response.css("#titleStoryLine").css("div")
            item['summary'] = title_story_line_block[1].css("p").css("span::text").get().strip()
            item['plot_keywords'] = title_story_line_block[2].css("a").css("span::text").extract()
            return item
        except Exception as e:
            print(f"Unable to scrape: {response.css('title::text')}")



