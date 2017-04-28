import scrapy
import urllib
import gzip
from bs4 import BeautifulSoup
from telsearch2.items import Telsearch2Item
from lxml import html
#from guppy import hpy


class AvitoSpider(scrapy.Spider):
    name = "mainspider5"
    custom_settings = {
        'DOWNLOAD_DELAY' : 2,
        'MEMUSAGE_ENABLED': 1
    }
    NAMEXP  = ".//tr/td[not(@class)]/h1/text()"
    #PHONEXP = ".//tr/td[not(@class)]/div/table/tr/td[2]/span/a/text()"
    TELEFON = ".//table[@class='sl-contact-table']/tr[td='Phone']/td[2]/span/a/text()"
    TELEFON = ".//table[@class='sl-contact-table']/tr[td='Telefon']/td[2]/span/a/text()"
    TELOCPT = ".//tr/td[not(@class)]/div[@class='tel-occupation']/text()"
    STRADRS = ".//td//span[@class='adr']/span[@class='street-address']/text()"
    POSTCOD = ".//td//span[@class='adr']/span[@class='tel-zipcity']/span[@class='postal-code']/text()"
    LOCALTY = ".//td//span[@class='adr']/span[@class='tel-zipcity']/span[@class='locality']/text()"
    POBOX   = ".//td//span[@class='pobox']/text()"
    REGION  = ".//td//span[@class='adr']/span[@class='tel-zipcity']/span[@class='region']/text()"
    FAXXP   = ".//table[@class='sl-contact-table']/tr[td='Fax']/td[2]/span/a/text()"
    MOBILE  = ".//table[@class='sl-contact-table']/tr[td[contains(.,'Mobile')]]/td[2]/span/a/text()"
    EMAIL   = ".//td[@class='tel_email']/*"
    EMAIL   = ".//a[@id='tel_email_0']/text()"
    WEBSITE = ".//table[@class='sl-contact-table']/tr[td[contains(.,'Link')]]/td/a/@href"
    CATEGRY = ".//div[@class='tel-detail-categories']/div[@class='tel-categories']/span//text()"
    PERSON  = ".//td//div[@class='tel-detail-categories']/following-sibling::span/text()"
    REGSTRY = ".//a[@class='sl-button sl-icon-tel-registry']/@href"
    
    def start_requests(self):
        urls = ['https://tel.search.ch/sitemap/sitemap_business_de_00'+str(i)+'.xml.gz' for i in range(0,10)]
        for url in urls: #to remove [] when golive
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        filename = response.url.split("/")[-1]
        filetoget = urllib.URLopener()
        filetoget.retrieve(response.url, filename)
        print "********Recieved file:", filename
        with gzip.open(filename, 'rb') as fr:
            file_content = fr.read()
            soup = BeautifulSoup(file_content,'lxml')
            links = soup.find_all('loc')
            #links = [
            #"https://tel.search.ch/kuesnacht/hoehenstrasse-28/weber-oertli-architekt-in",
            #"https://tel.search.ch/detligen/gewerbegasse-29/markwalder-shiatsu-tai-ji-qigong",
            #"https://tel.search.ch/basel/aeschenvorstadt-67/simonius-partner"]
            #link_list = []
            for link in links: #to remove [] when golive
                link = str(link).replace('<loc>','').replace('</loc>','') + ".de.html"
                #link_list.append(link)
                yield scrapy.Request(url=link, headers=headers, callback=self.parse2)
        print "********Links extracted:",filename
        #self.log('Saved file %s' % filename)

    def parse2(self, response):

        #harvstd = html.fromstring(response.body)
        response.selector.remove_namespaces()
        name    = '|'.join(response.xpath(self.NAMEXP).extract()).encode("utf-8")
        pageurl = response.url
        #telefon = harvstd.xpath(TELEFON)
        telefon = response.selector.remove_namespaces().xpath(self.TELEFON).extract()
        telocp  = response.selector.remove_namespaces().xpath(self.TELOCPT).extract()
        straddr = response.selector.remove_namespaces().xpath(self.STRADRS).extract()
        postcod = response.selector.remove_namespaces().xpath(self.POSTCOD).extract()
        localty = response.selector.remove_namespaces().xpath(self.LOCALTY).extract()
        pobox   = response.selector.remove_namespaces().xpath(self.POBOX).extract()
        region  = response.selector.remove_namespaces().xpath(self.REGION).extract()
        fax     = response.selector.remove_namespaces().xpath(self.FAXXP).extract()
        mobile  = response.selector.remove_namespaces().xpath(self.MOBILE).extract()
        email   = response.selector.remove_namespaces().xpath(self.EMAIL).extract()
        website = response.selector.remove_namespaces().xpath(self.WEBSITE).extract()
        categry = response.selector.remove_namespaces().xpath(self.CATEGRY).extract()
        person  = response.selector.remove_namespaces().xpath(self.PERSON).extract()
        regstry = ''.join(response.xpath(self.REGSTRY).extract()).split('http://')[-1]
        
        item = Telsearch2Item()
        item["name"]    = name
        item["telefon"] = telefon
        item["url"]     = pageurl
        item["telocp"]  = telocp
        item["straddr"] = straddr
        item["postcod"] = postcod
        item["localty"] = localty
        item["pobox"]   = pobox
        item["region"]  = region
        item["fax"]     = fax
        item["mobile"]  = mobile
        item["email"]   = email
        item["website"] = website
        item["categry"] = categry
        item["person"] = person
        item["regstry"] = regstry
        yield item