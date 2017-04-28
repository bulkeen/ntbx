import scrapy
import urllib
import gzip
from bs4 import BeautifulSoup
from telsearch2.items import Telsearch2Item
from lxml import html
from guppy import hpy


class AvitoSpider(scrapy.Spider):
    name = "spider2"
    custom_settings = {
        'DOWNLOAD_DELAY' : 4
    }
    def start_requests(self):
        urls = ['https://tel.search.ch/sitemap/sitemap_business_de_00'+str(i)+'.xml.gz' for i in range(0,10)]
        for url in urls[5:9]: #to remove [] when golive
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        filename = response.url.split("/")[-1]
        filetoget = urllib.URLopener()
        filetoget.retrieve(response.url, filename)
        print "********Recieved file:", filename
        with gzip.open(filename, 'rb') as fr:
            #print "********Heap at the start:\n", hp.heap()
            file_content = fr.read()
            soup = BeautifulSoup(file_content,'lxml')
            links = soup.find_all('loc')
            #links = [
            #"https://tel.search.ch/kuesnacht/hoehenstrasse-28/weber-oertli-architekt-in",
            #"https://tel.search.ch/detligen/gewerbegasse-29/markwalder-shiatsu-tai-ji-qigong",
            #"https://tel.search.ch/basel/aeschenvorstadt-67/simonius-partner"]
            link_list = []
            for link in links: #to remove [] when golive
                link = str(link).replace('<loc>','').replace('</loc>','') + ".de.html"
                link_list.append(link)
                yield scrapy.Request(url=link, headers=headers, callback=self.parse2)
        print "********Links extracted:",filename
        #with open("Links_list.txt", "ab") as fw:
        #    for i in link_list: fw.write(i+"\n")
        self.log('Saved file %s' % filename)

    def parse2(self, response):
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

        harvstd = html.fromstring(response.body)
        name    = '|'.join(harvstd.xpath(NAMEXP)).encode("utf-8")
        pageurl = response.url
        telefon = harvstd.xpath(TELEFON)
        telocp  = harvstd.xpath(TELOCPT)
        straddr = harvstd.xpath(STRADRS)
        postcod = harvstd.xpath(POSTCOD)
        localty = harvstd.xpath(LOCALTY)
        pobox   = harvstd.xpath(POBOX)
        region  = harvstd.xpath(REGION)
        fax     = harvstd.xpath(FAXXP)
        mobile  = harvstd.xpath(MOBILE)
        email   = harvstd.xpath(EMAIL)
        website = harvstd.xpath(WEBSITE)
        categry = harvstd.xpath(CATEGRY)
        person  = harvstd.xpath(PERSON)
        regstry = ''.join(harvstd.xpath(REGSTRY)).split('http://')[-1]
        
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