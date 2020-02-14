import codecs
from lxml import html
import requests
# this needs to work for both
page = requests.get("http://127.0.0.1:5500/leboncoin/case.html")
#page2 = requests.get("https://www.leboncoin.fr/recherche/?category=9&locations=Cassis_13260")
assert page is not None
tree = html.fromstring(page.content)
assert tree is not None

# Find xpath for Title of Annonce
# returns a list of titles
print("X-path for title of annonce\n")
title_path = tree.xpath(
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[1]/p/span/text()'
)
print(title_path)
print("\n")
# Find x path for price of Annonce
# returns an array of prices
print("X-path for price of annonce\n")
price_path = tree.xpath(
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[1]/div/span/span/text()'
)
price_data = [r.rstrip("\xa0â\x82¬")
              for r in price_path]

print(price_data)
print("\n")
# Find XPath for kind of annonce (“Pro”, bold)
kind_data = tree.xpath(
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[2]/p/span/text()'
)
print("X-path for kind of annonce\n")
kind_data = [r.strip("()")for r in [r.rstrip("\xa0â\x82¬")
                                    for r in kind_data]]   # this can be an abstract method
print(kind_data)
print("\n")

# Find XPath for type of annonce (“Ventes Immobilières”)
print("X-path for type of annonce\n")
type_data = tree.xpath(
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[2]/p[1]/text()')
# strip down /clean list
print(list(filter(lambda x: x != '', [r.rstrip() for r in type_data])), "\n")
# 1.e Find XPath
# 1.f Find XPath for zip code of annonce
city_zip_data = tree.xpath(
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[2]/p[2]/text()'
)
cities_and_zip_code = [r.split(" ") for r in city_zip_data]

print("X path for city and  zip code\n")
print(cities_and_zip_code, "\n")

# 1.g Find XPath for date
date_data = tree.xpath(
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li[9]/a/section/div[2]/p[3]/text()'
)
print("X path for date\n")
print(date_data)
