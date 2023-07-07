import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["rokomari.com"]
    start_urls = ["http://rokomari.com/book/authors"]
    custom_settings = {'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'}

    def parse(self, response):
        authors=response.css('ul.authorList li a')

        for author in authors:
            yield{
                'authorName': author.css('h2 ::text').get()
            }

        selectors = response.css('a')
        next_link = selectors.css('a:contains("next")')
        nextPageAuthorList = next_link.css('::attr(href)').get()
        print(nextPageAuthorList)

        if nextPageAuthorList is not None:
            nextPageAuthorUrl='http://rokomari.com'+nextPageAuthorList
            print('next page url author list --------------------->')
            print(nextPageAuthorUrl)
            yield response.follow(nextPageAuthorUrl,callback=self.parse)

