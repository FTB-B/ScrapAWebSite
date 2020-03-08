import scrapy
from ..items import DonalwinItem

class DonalWinTweets(scrapy.Spider):
    name = 'donaldwin' # the name of our Spider
    start_urls = ['https://thedonald.win/']
    #start_urls =['https://thedonald.win/p/4Ap0tUc/aoc-complains-wages-arent-rising/c/']

    
    def parse(self, response):
        
        #print(len(start_urls))
        items = DonalwinItem()
        items_output = []
        print("1111111111111111111111111111111111111111111111111111111")
        
        comments_url = response.css("div.actions a.comments::attr(href)").getall()
        print(comments_url[1])
        print(len(comments_url))
        for comment_url in comments_url:
            #output1 =yield scrapy.Request(response.urljoin(comment_url),callback = self.parse_comments, meta={'item':items})
            output1 =  yield scrapy.Request("https://thedonald.win"+str(comment_url), callback=self.parse_comments)
            print(output1)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            items_output.append(output1)
        next_page = response.css("div.more a").xpath("@href").extract()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link,callback= self.parse)
        #print("next page: " + str(next_url))
        
        
        #response.follow(comments_url[2],callback= self.parse_comments)
        #request =  scrapy.Request("https://thedonald.win"+comments_url[2], callback=self.parse_comments, meta={'item' : items})
        '''
        for comment_url in comments_url:
            #output1 =yield scrapy.Request(response.urljoin(comment_url),callback = self.parse_comments, meta={'item':items})
            output1 =  yield scrapy.Request("https://thedonald.win"+str(comment_url), callback=self.parse_comments, meta={'item':items})
            print(output1)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            items_output.append(output1)

        '''
        # for comment_url in comments_url:
        #     print("00000000000000")
        #     output1 = self.parse_comments2(response,comment_url)
        #     print(output1)      
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(items_output)
        # return 
        '''

        post_title = response.css('a.title::text').extract()
        post_href = response.css('a.title').xpath("@href").extract()
        #post_author = response.css('a.author::text').extract()
        post_author = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "since", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]/text()').extract()
        post_vote = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "count", " " ))]//text()').extract()
        #post_body = response.css('div.content.text::text').extract()
        post_time = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "post", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "timeago", " " ))]').extract()
        post_comments_authors = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "comment", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]').extract()
        #print(post_comments_authors
        comments = []
        for i in response.css('.comment-list > .comment:nth-child(n)').extract():
            print(i)
            sel = scrapy.Selector(text = str(i))
            comment_author1 = sel.css('.author::text').extract()
            print(comment_author1)
            child_author= sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "child", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]/text()').extract()
            print(child_author)
            post_i = sel.css('.comment .body').extract()
            print(post_i)
            
            for pp in post_i:
                print(pp)
                sel2 = scrapy.Selector(text = str(pp))
                comment_author = sel2.css('a.author::text').extract()
                #print(comment_author[0])
                comment_parent = ""
                print(child_author)
                if(comment_author[0] in child_author):
                    print("###########################it is a child########################################")
                    comment_parent = comment_author1[0]
                
                comment_content = sel2.css('p').extract()
                print(comment_content)
                comment_point = sel2.css('.points::text').extract()
                print(comment_point)
                comment_time = sel2.css('.timeago').extract()
                print(comment_time)
                comments.append([{
                    'comment_author' : comment_author,
                    'comment_parent' : comment_parent,
                    'comment_content' : comment_content,
                    'comment_time' : comment_time,
                    'comment_point' : comment_point,
                }]
                )
                
            #comment_author = sel.css('.author::text').extract()
            #child_author= sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "child", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]/text()').extract()
            #print(comment_author)
            #print(child_author)
            #comment_content = sel.css('p').extract()
            #print(comment_content)
            #comment_point = sel.css('.points::text').extract()
            #print(comment_point)
            #comment_time = sel.css('.timeago').extract()
            #print(comment_time)
            print("###########################################################")
        # comment_level1 = response.css('.comment-list > .comment:nth-child(2) .comment p').extract()
        # print(comment_level1)
        # for comm in comment_level1:
        #     print(comm)
        #     print("###############################################################")
        # for i in response.css('.comment-list > .comment:nth-child(n+1) .comment p'):
        #     print(''.join(i.xpath('descendant-or-self::text()').extract())) 
        #     print("************************************************************************")
    
    #     post_comments_1 = response.css('.comment-list > .comment .body').extract()
    #     count = 1
    #     for pp in post_comments_1:
    #         print(pp)
    #         sel = scrapy.Selector(text = str(pp))
    #         comment_author = sel.css('a.author::text').extract()
    #         print(comment_author)
    #         comment_content = sel.css('p').extract()
    #         print(comment_content)
    #         comment_point = sel.css('.points::text').extract()
    #         print(comment_point)
    #         comment_time = sel.css('.timeago').extract()
    #         print(comment_time)
    #         print("***************************************************")
    #    # print(post_comments_1)
        items['post_1title'] = post_title
        items['post_2href'] = post_href
        items['post_3author'] = post_author
        items['post_4vote'] = post_vote
        items['post_5time'] = post_time
        items['post_6comments'] = comments

        yield items

        # yield {
        #     'post_title' : post_title,
        #     'post_href' :post_href,
        #     'post_author': post_author,
        #     'post_vote' : post_vote,
        #     'post_time' : post_time,
        #     'post_comments': comments,
        #     }



        next_page = response.css("div.more a::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
     
        '''
    def add_start_urls(self,response):
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        next_url = response.css("div.more a").xpath("@href").extract()
        print(next_url)
        print(response.url)
        start_urls.append(response.url)
        if next_url is not None:
            yield response.follow(start_urls[0]+next_url[0],callback = self.add_start_urls)
    
    def parse_comments(self, response):
        items = DonalwinItem()
        #items = response.meta['item']
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&7")
        post_title = response.css('a.title::text').extract()
        print(post_title)
        post_href = response.css('a.title').xpath("@href").extract()
        print(post_href)
        #post_author = response.css('a.author::text').extract()
        post_author = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "since", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]/text()').extract()
        print(post_author)
        post_vote = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "count", " " ))]//text()').extract()
        print(post_vote)
        #post_body = response.css('div.content.text::text').extract()
        post_time = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "post", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "timeago", " " ))]').extract()
        post_comments_authors = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "comment", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]').extract()
        print(len(post_comments_authors))
        comments = []
        for i in response.css('.comment-list > .comment:nth-child(n)').extract():
            #print(i)
            sel = scrapy.Selector(text = str(i))
            comment_author1 = sel.css('.author::text').extract()
            #print(comment_author1)
            child_author= sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "child", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]/text()').extract()
            #print(child_author)
            post_i = sel.css('.comment .body').extract()
            #print(post_i)
            
            for pp in post_i:
                #print(pp)
                sel2 = scrapy.Selector(text = str(pp))
                comment_author = sel2.css('a.author::text').extract()
                print(comment_author)
                comment_parent = ""
                #print(child_author)
                if(len(comment_author) == 0):
                    break
                if(comment_author[0] in child_author):
                    print("###########################it is a child########################################")
                    comment_parent = comment_author1[0]
                    print("parent =" + comment_parent)
                
                comment_content = sel2.css('p').extract()
                #print(comment_content)
                comment_point = sel2.css('.points::text').extract()
                #print(comment_point)
                comment_time = sel2.css('.timeago').extract()
                #print(comment_time)
                comments.append([{
                    'comment_author' : comment_author,
                    'comment_parent' : comment_parent,
                    'comment_content' : comment_content,
                    'comment_time' : comment_time,
                    'comment_point' : comment_point,
                }]
                )
        print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")        
        items['post_1title'] = post_title
        items['post_2href'] = post_href
        items['post_3author'] = post_author
        items['post_4vote'] = post_vote
        items['post_5time'] = post_time
        items['post_6comments'] = comments
        #print(items)

        yield items

    def parse_comments2(self, response, url):
        items1 = DonalwinItem()
        #items = response.meta['item']
        print(url)
       # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&7")
        request = scrapy.Request(response.urljoin(url),callback = self.parse_comments, meta={'item':items1})
        yield request
        return items1
