# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import json
import os
from scrapy.exporters import PythonItemExporter

from .constants import Constants


class ImdbdatacrawlerPipeline:
    def _get_exporter(self, **kwargs):
        return PythonItemExporter(binary=False, **kwargs)

    def __init__(self):
        self.exporter = self._get_exporter()
        self.movie_dump = None

    def open_spider(self, spider):
        self.movie_dump = open(Constants.MOVIE_JSON_DUMP.value, "w+")
        self.movie_dump.write('[')

    def process_item(self, item, spider):
        json_dumps_str = f"{json.dumps(self.exporter.export_item(item))},"
        self.movie_dump.write(json_dumps_str)

    def close_spider(self, spider):
        self.movie_dump.seek(self.movie_dump.tell()-1, os.SEEK_SET)
        self.movie_dump.truncate()
        self.movie_dump.write(']')
        self.movie_dump.close()
