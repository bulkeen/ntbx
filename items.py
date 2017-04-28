# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Telsearch2Item(scrapy.Item):
    # define the fields for your item here like:
	name	= scrapy.Field()
	telefon	= scrapy.Field()
	#pageurl	= scrapy.Field()
	telocp	= scrapy.Field()
	straddr	= scrapy.Field()
	postcod	= scrapy.Field()
	localty	= scrapy.Field()
	pobox	= scrapy.Field()
	region	= scrapy.Field()
	fax		= scrapy.Field()
	mobile	= scrapy.Field()
	email	= scrapy.Field()
	url		= scrapy.Field()
	website = scrapy.Field()
	categry	= scrapy.Field()
	person	= scrapy.Field()
	regstry	= scrapy.Field()