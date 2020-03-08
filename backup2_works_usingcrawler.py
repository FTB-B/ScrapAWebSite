import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import DonalwinItem

class DonalWinTweets(CrawlSpider):
    name = 'donaldwin' # the name of our Spider
    max_retries = 4
    start_urls = ['https://thedonald.win/?page=1']
   #start_urls = ['https://thedonald.win/p/469S7LG/weve-put-the-subreddit-in-restri/']
    base_url = 'https://thedonald.win/'
    

    rules = [Rule(LinkExtractor(allow = 'https://thedonald.win/?', deny = ['https://thedonald.win/new','https://thedonald.win/top','https://thedonald.win/rising']), callback= 'parse_filter_comments', follow=True)]
    

    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retries = {}

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            meta={
                'handle_httpstatus_list': [302],
            },
        )

    def parse(self, response):
        # if response.status == 302:
        #     retries = self.retries.setdefault(response.url, 0)
        #     if retries < self.max_retries:
        #         self.retries[response.url] += 1
        #         yield response.request.replace(dont_filter=True)
        #     else:
        #         self.logger.error('%s still returns 302 responses after %s retries',response.url, retries)    
        # return                      
        #print(len(start_urls))
        items = DonalwinItem()
        items_output = []
        print("1111111111111111111111111111111111111111111111111111111")
        
        comments_url = response.css("div.actions a.comments::attr(href)").getall()
        print(len(comments_url))
        #print(comments_url[])
        
        for comment_url in comments_url:
            comment_link_url = self.base_url+comment_url
            #output1 =yield scrapy.Request(response.urljoin(comment_url),callback = self.parse_comments, meta={'item':items})
            yield scrapy.Request(comment_link_url, callback=self.parse_comments)
           
        
        next_page = response.css("div.more a").xpath("@href").getall()
        print(next_page)
        print("*****************************************************************************")
        if len(next_page) == 1:
            next_page_url = self.base_url + next_page[0]
            yield scrapy.Request(next_page_url, callback= self.parse)
            print(next_page_url)
        else:
            next_page_url = self.base_url + next_page[1]
            print(next_page_url)
            yield scrapy.Request(next_page_url,meta = {
                  'dont_redirect': True,
                  'handle_httpstatus_list': [302]
              }, callback= self.parse)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")  

        '''
 
    def parse_filter_comments(self, response):

        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        comment_page = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "more", " " ))]//a').extract()
        if(not comment_page):
            post_title = response.css('a.title::text').extract()
            #print(post_title)
            post_href = response.css('a.title').xpath("@href").extract()
            #print(post_href)
            #post_author = response.css('a.author::text').extract()
            post_author = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "since", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]/text()').extract()
            #print(post_author)
            post_vote = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "count", " " ))]//text()').extract()
            #print(post_vote)
            #post_body = response.css('div.content.text::text').extract()
            post_time = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "post", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "timeago", " " ))]').extract()
            #post_total_comments = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "total", " " ))]//text()').extract().strip()
            post_total_comments = response.css("a.comments::text").extract()
            post_comments_authors = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "comment", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]').extract()
            #print(len(post_comments_authors))
            #comments_level1 = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "comment-list", " " ))]//>//*[contains(concat( " ", @class, " " ), concat( " ", "comment", " " ))]').extract()
            #for comment_l1 in comments_level1:
            #
            comments = []
            
            for i in response.css('.comment-list > .comment:nth-child(n)').extract():
                #print(i)
                sel = scrapy.Selector(text = str(i))
                comment_author1 = sel.css('.author::text').extract()
                #print(comment_author1)
                child_author= sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "child", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "author", " " ))]/text()').extract()
                                        #'//*[contains(concat( " ", @class, " " ), concat( " ", "child", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "child", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "body", " " ))]'
                #print(child_author)
                post_i = sel.css('.comment .body').extract()
                #print(post_i)
                
                for pp in post_i:
                    #print(pp)
                    sel2 = scrapy.Selector(text = str(pp))
                    comment_author = sel2.css('a.author::text').extract()
                    #print(comment_author)
                    comment_parent = ""
                    #print(child_author)
                    if(len(comment_author) == 0):
                        break
                    if(comment_author[0] in child_author):
                        #print("###########################it is a child########################################")
                        comment_parent = comment_author1[0]
                        #print("parent =" + comment_parent)
                    
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
            #print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")   
            items = DonalwinItem()     
            items['post_1title'] = post_title
            items['post_2href'] = post_href
            items['post_3author'] = post_author
            items['post_4vote'] = post_vote
            items['post_5time'] = post_time
            items['post_6total_comments'] = post_total_comments
            items['post_7comments'] = comments
            # #print(items)

            yield items
            # yield{
            #     'post_1title' : post_title,
            #     'post_2href' : post_href,
            #     'post_3author' : post_author,
            #     'post_4vote' : post_vote,
            #     'post_5time' : post_time,
            #     'post_6comments' : comments,
            # }
        else:
            print(response.url)    
