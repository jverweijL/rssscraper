from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_escape_chars

class TendernedLoader(ItemLoader):

    default_output_processor = TakeFirst()

    title_in = MapCompose(lambda v: v.split())
    title_out = Join()

    content_in = MapCompose(unicode.lower,remove_tags, lambda v: v.split())
    content_out = Join()