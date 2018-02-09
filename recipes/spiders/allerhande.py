# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import SitemapSpider

from ..items import RecipeItem

def safe_first(items, fn=lambda x: x):
    result = (items or [None])[0]
    return fn(result) if result is not None else result

class AllerhandeSpider(SitemapSpider):
    name = 'allerhande'

    sitemap_urls = ['http://www.ah.nl/static/recipe-sitemap.xml']
    allowed_domains = ['ah.nl']

    sitemap_rules = [
        ('/allerhande/recept/', 'parse_recipe'),
    ]

    def parse_recipe(self, response):
        item = RecipeItem()
        item['location'] = response.url
        item['name'] = safe_first(
            response.css('section.header > header.header-inner > h1::text').extract(),
            lambda nm: nm.replace('\xad', ''))

        item['header_image'] = safe_first(response.css(
            'section.teaser > ul.carousel.carousel--no-transform > li.responsive-image::attr(data-default-src)'
            ).extract())

        item['header_image_mobile'] = safe_first(response.css(
            'section.teaser > ul.carousel.carousel--no-transform > li.responsive-image::attr(data-phone-src)'
            ).extract())

        item['tags'] = response.css(
            'section.teaser > ul.carousel.carousel--no-transform > li.responsive-image > div.wrapper > section.info.hidden-phones > ul.tags > li > a::text'
            ).extract()

        item['course'] = safe_first(response.css(
            'section.teaser > ul.carousel.carousel--no-transform > li.responsive-image > div.wrapper > section.info.hidden-phones > ul.short > li > div.icon.icon-course + span::text'
            ).extract())

        item['calories'] = safe_first(response.css(
            'section.teaser > ul.carousel.carousel--no-transform > li.responsive-image > div.wrapper > section.info.hidden-phones > ul.short > li > div.icon.icon-nutritional + span::text'
            ).extract())

        item['ingredient_search_terms'] = response.css(
            'section.js-ingredients.ingredients > ul.list.shopping.ingredient-selector-list > li[itemprop=ingredients] > a::attr(data-search-term)'
            ).extract()

        item['ingredient_singular'] = response.css(
            'section.js-ingredients.ingredients > ul.list.shopping.ingredient-selector-list > li[itemprop=ingredients] > a::attr(data-description-singular)'
            ).extract()

        item['ingredient_display'] = response.css(
            'section.js-ingredients.ingredients > ul.list.shopping.ingredient-selector-list > li[itemprop=ingredients] > a > span::text'
            ).extract()

        item['steps'] = response.css(
            'section.preparation[itemprop=recipeInstructions] > ol > li::text, section.preparation[itemprop=recipeInstructions] > p::text'
            ).extract()

        return item
