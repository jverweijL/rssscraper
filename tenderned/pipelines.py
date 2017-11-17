# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging, json, requests, hashlib
logger = logging.getLogger(__name__)
logger.warning("This is a warning")

class TendernedPipeline(object):
    def process_item(self, item, spider):
        return item

class LiferayArticleImporterPipeline(object):
    def process_item(self, item, spider):
        
        title = b'{{"en_US":"{0}"}}'.format(item['title'])
        content = b'<?xml version="1.0"?><root available-locales="en_US" default-locale="en_US"><dynamic-element name="content" type="text_area" index-type="text" instance-id="bbau"><dynamic-content language-id="en_US"><![CDATA[<p>{1}</p><p>{0}</p>]]></dynamic-content></dynamic-element></root>'.format(item['content'].encode('utf8', 'ignore'),item['url'])
        uid = hashlib.md5(item['url'].encode("utf8")).hexdigest()

        headers = {}
        payload = {'groupId':231145,
                   'folderId':231159,
                   'classNameId':0,
                   'classPK':0,
                   'articleId':uid,
                   'autoArticleId':'false',
                   'titleMap':title,
                   'descriptionMap': '{"en_US":"none"}',
                   'content': content,
                   'ddmStructureKey':'BASIC-WEB-CONTENT',
                   'ddmTemplateKey':'BASIC-WEB-CONTENT',
                   'layoutUuid':'',
                   'displayDateMonth':1,
                   'displayDateDay':1,
                   'displayDateYear':2017,
                   'displayDateHour':1,
                   'displayDateMinute':1,
                   'expirationDateMonth':1,
                   'expirationDateDay':1,
                   'expirationDateYear':2019,
                   'expirationDateHour':1,
                   'expirationDateMinute':1,
                   'neverExpire':'false',
                   'reviewDateMonth':0,
                   'reviewDateDay':0,
                   'reviewDateYear':0,
                   'reviewDateHour':0,
                   'reviewDateMinute':0,
                   'neverReview':'true',
                   'indexable':'true',
                   'articleURL':''}

        logger.info("Payload: %s",payload)

        r = requests.post("http://localhost:8080/api/jsonws/journal.journalarticle/add-article", auth=('test@liferay.com', 'password'), data=payload, headers=headers)
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('/tmp/items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item