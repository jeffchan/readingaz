from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from readingaz.items import Book
import re
import os

USERNAME = 'bakinder'
PASSWORD = 'kinder2011'

class ReadingazSpider(CrawlSpider):
	name = "readingaz"
	allowed_domains = ['readinga-z.com']
	#start_urls = ['http://www.readinga-z.com/book/leveled-books.php']

	rules = (
	    # Extract links matching 'book.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('book\.php', )), callback='parse_book'),
    )



	def start_requests(self):
  		return [FormRequest("http://www.readinga-z.com/auth/login.php",
                        formdata={'username': USERNAME, 'password': PASSWORD},
                        callback=self.logged_in)]

  	def parse_book(self, response):

  		hxs = HtmlXPathSelector(response)
  		url = response.url
  		title = hxs.select('//h1/text()').extract()[0]
		level = hxs.select('//ul/li/a[contains(@class, "active")]/text()').re(r'Level\s*(.*)')[0]
		
		pdfs = []

		links = hxs.select('//a[contains(@href, "members")]')
		for link in links :
			if len(link.select(".//text()").re(r'Single-Sided Book')) > 0 :
				pdfs.append(link.select("@href").extract()[0])
			if len(link.select(".//text()").re(r'All Worksheets')) > 0 :
				pdfs.append(link.select("@href").extract()[0])

		#self.log("parse_book %s %s" % (title , level))

		for url in pdfs :
			level = url.split('/')[-2]
			if 'span' in level or 'fr' in level or 'uk' in level:
				continue
			yield Request('http://www.readinga-z.com'+url, callback=self.save_pdf)

		# item = Book()
		# item['url'] = url
		# item['title'] = title
		# item['level'] = level
		# item['pdfs'] = pdfs

		# return item
	
	def save_pdf(self, response):
		filepath = self.get_path(response.url.split('/')[-1])
		print 'writing to ... ' + filepath
		with open(filepath, "wb") as f:
			f.write(response.body)

	def get_path(self, url):
		name = re.search(r'raz(\w+)\.pdf', url).group(0)
		level = re.search(r'(?<=raz_l)[A-Za-z]+', name).group(0)
		num = re.search(r'(?<=raz_l[A-Za-z])\d+', name)
		if (num is None) :
			num = re.search(r'(?<=raz_l[A-Za-z]{2})\d+', name)
		id = num.group(0)
		#dir = 'files/'+level+'/'+id
		dir = 'files/'+level
		if not os.path.exists(dir):
			os.makedirs(dir)
		return dir+'/'+name

	def logged_in(self, response):
		self.log("Visited %s" % response.url)
		return Request('http://www.readinga-z.com/book/leveled-books.php', callback=self.parse)
		