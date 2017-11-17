# -*- coding: utf-8 -*-
import scrapy,string

from scrapy.spiders import XMLFeedSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector,SelectorList
from scrapy.http import HtmlResponse
from tenderned.itemloaders import TendernedLoader
from tenderned.items import TendernedItem


class TendernedspiderSpider(XMLFeedSpider):
    name = 'tendernedspider'
    allowed_domains = ['tenderned.nl']
    start_urls = ['https://www.tenderned.nl/tenderned-rss-web/rss/laatste-publicatie.rss']
    namespaces = [
        ('atom', 'http://www.w3.org/2005/Atom'),
    ]
    custom_settings = {'CLOSESPIDER_PAGECOUNT':100,'DOWNLOAD_DELAY':2}
    iterator = 'xml'
    itertag = 'atom:entry'
    
    def parse_node(self, response, node):
        link = node.xpath('atom:link/@href').extract()[0]
        link = string.replace(link,'/detail/samenvatting/','/detail/publicatie/')
        self.logger.info('link: %s', link)
        request = scrapy.Request(link, callback=self.parse_page)
        yield request

    def parse_page(self, response):
        self.logger.info('Time to parse item url: %s', response.url)

        l = TendernedLoader(item=TendernedItem(), response=response)
        l.add_value('url',response.url)
        l.add_xpath('title', '//div[@id="content"]/h1/text()')
        l.add_xpath('content', '//div[@id="content"]/form/descendant::*/text()')
        return l.load_item()
