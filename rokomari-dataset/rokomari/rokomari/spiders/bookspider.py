import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["rokomari.com"]
    start_urls = ["http://rokomari.com/book/authors"]
    custom_settings = {'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'}

    def parse(self, response):
        authors=response.css('ul.authorList li a')

        for author in authors:
            allbook=author.css('a').attrib['href']
            allbookUrl='https://www.rokomari.com/'+allbook
            # called another function
            yield response.follow(allbookUrl,callback=self.SingleAuthorAllBook)

        nextPageAuthorList=response.css('.pagination a::attr(href)').get()
        print(nextPageAuthorList)


        if nextPageAuthorList is not None:
            nextPageAuthorUrl='http://rokomari.com'+nextPageAuthorList
            print('next page url author list --------------------->')
            print(nextPageAuthorUrl)
            yield response.follow(nextPageAuthorUrl,callback=self.parse)




    def SingleAuthorAllBook(self,response):
        allbooks=response.css('.book-list-wrapper')
        
        for allbook in allbooks:
            singleBookUrl=allbook.css('a').attrib['href']
            singleBookRedirectUrl='https://www.rokomari.com/'+singleBookUrl
            print(singleBookUrl)
            yield{
                'bookName': singleBookUrl
            }

        nextPageBookList=response.css('.pagination a::attr(href)').get()

        if nextPageBookList is not None:
            SingleAuthorNextPageBook='http://rokomari.com'+nextPageBookList
            yield response.follow(SingleAuthorNextPageBook,callback=self.parse)

