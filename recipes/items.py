# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipeItem(scrapy.Item):
    # define the fields for your item here like:
    location = scrapy.Field()
    name = scrapy.Field()
    header_image = scrapy.Field()
    header_image_mobile = scrapy.Field()
    tags = scrapy.Field()
    course = scrapy.Field()
    calories = scrapy.Field()
    ingredient_search_terms = scrapy.Field()
    ingredient_singular = scrapy.Field()
    ingredient_display = scrapy.Field()
    steps = scrapy.Field()