import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags, remove_tags_with_content

class BloombergSpider(CrawlSpider):
    name = "Bloomberg"
    start_urls = ["http://bloomberg.com/"]

    rules = (Rule(LinkExtractor(allow=r"bloomberg.com/news/article"), callback='parse_dir_contents', follow=True),)

    def parse_dir_contents(self, response):
        title_class = ".lede-headline__highlighted"
        title = response.selector.css(title_class).xpath("text()").extract()
        article_content_class = ".article-body__content"
        content = response.selector.css(article_content_class).xpath('.//p').extract()

        if not content:
            fallback_class = ".body-copy"
            content = response.selector.css(fallback_class).xpath('.//p').extract()

        article = "".join(content)
        article = remove_tags(remove_tags_with_content(article, ('script',)))
        url = response.url

        # 2016-11-22T05:15:42.847Z
        date = response.selector.xpath('//main//time//@datetime').extract()


        yield {
            'url': response.url,
            'date': date,
            'title': title,
            'article': article
        }