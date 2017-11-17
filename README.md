# Scrape mentioned in rss feeds and store the in Liferay

## Requirements

* [scrapy](https://doc.scrapy.org)
* [requests lib](http://docs.python-requests.org/en/master/)

## Setup
### Spider
Within the spider (tendernedspider.py) you can control things like start url, number of pages to download, throttle, etc.
With the variable itertag you can define the name of the tag for each entry in the rss feed.
The function parse_node will parse the itertag and you can add the links to the spider as new pages to fetch and set a callback to parse these pages.

parse_page will collect all the information from a page and store it into an TendernedItem
 
### Pipelines
Once items are found they are sent to the pipelines. In settings.py you can see which pipelines are enabled. E.g. you can create a pipeline for fetching documents and submitting them to Liferay, database or elasticsearch (or all of them). Or add a specific pipeline to add tags or additional metadata after storing them in Liferay.
 
In this example we have the LiferayArticleImporterPipeline and call the rest api to store data into a specific site. 

```
r = requests.post("http://localhost:8080/api/jsonws/journal.journalarticle/add-article", auth=('test@liferay.com', 'password'), data=payload, headers=headers)
```

## Run
To run this scrapy you can use:
```
scrapy crawl tendernedspider
```
