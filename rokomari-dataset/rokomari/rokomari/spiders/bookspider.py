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



        selectors = response.css('a')
        next_link = selectors.css('a:contains("next")')
        nextPageAuthorList = next_link.css('::attr(href)').get()
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
            yield response.follow(singleBookRedirectUrl,callback=self.collectData)


        selectors = response.css('a')
        next_link = selectors.css('a:contains("next")')
        nextPageBookList = next_link.css('::attr(href)').get()

        if nextPageBookList is not None:
            SingleAuthorNextPageBook='http://rokomari.com'+nextPageBookList
            yield response.follow(SingleAuthorNextPageBook,callback=self.parse)


    def collectData(self,response):
        table_rows=response.css('table tr')
        try:
            numberOfRating = int(response.css('.details-book-info__content-rating span::text').get().strip().split()[0])
        except (AttributeError, ValueError):
            numberOfRating = None

        

        try:
            numberOfReview=int(response.css('.details-book-info__content-rating span a::text').get().strip().split()[0])
        except (AttributeError,ValueError):
            numberOfReview=None

        
        try:
            summery=response.css('.tab-content .details-book-additional-info__content-summery .summary-description ::text').get()
        except (AttributeError,ValueError):
            summery=""

        try:
            orginalPrice=int(response.css('.details-book-info__content-book-price strike::text').get().strip().split()[1])
        except (AttributeError,ValueError):
            orginalPrice=0

        try:
            sellPrice=int(response.css('.details-book-info__content-book-price span::text').get().strip().split()[1])
        except (AttributeError,ValueError):
            sellPrice=0


        yield {
            "url": response.url,
            "title": table_rows[0].css('td::text').getall()[1],
            "author": table_rows[1].css('td a::text').get(),
            "publisher": table_rows[2].css('td  a::text').get(),
            "isbn": table_rows[3].css('td::text').getall()[1],
            "page" : table_rows[4].css('td::text').getall()[1],
            "country": table_rows[5].css('td::text').getall()[1],
            "language" :table_rows[6].css('td::text').getall()[1],
            "category" : response.css(".details-book-info__content-category a::text").get(),
            "rating":"",
            "numberOfRating": numberOfRating,
            "numberOfReview" : numberOfReview,
            "orginalPrice" :  orginalPrice,
            "sellPrice" :sellPrice,
            "summery": summery,
            "imageUrl" :response.css('.look-inside::attr(src)').get(),

        }

        